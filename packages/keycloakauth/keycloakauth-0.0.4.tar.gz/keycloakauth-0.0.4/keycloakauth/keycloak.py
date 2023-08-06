import requests
import time
import functools
import importlib

django_keycloak_auth = importlib.import_module("django-keycloak-auth.keycloak")


def token_decorator(func):
    @functools.wraps(func)
    def wrapper(kworker, *args, **kwargs):
        if time.time() >= kworker.token_expiration - 5:
            if time.time() >= kworker.refresh_token_expiration - 5:
                kworker.get_token(auth_data=kworker.auth_data)
            else:
                kworker.get_token(auth_data=kworker.auth_refresh_data)
        return func(kworker, *args, **kwargs)

    return wrapper


class KeycloakException(Exception):
    pass


class KeycloakWorker(django_keycloak_auth.KeycloakConnect):
    """
    Class:
        to introspect the token
        to check if the token is active and which roles it bears
        to get userinfo about the token owner
        to manage Keycloak Group membership

    Authentication and Authorization are based on Keycloak Roles:
    Role mapped to Group, User is a member of the Group.
    Roles:
      format: <IS name>:user:manage
      example: crux:user:manage
      example: all:user:manage

    Groups:
      format: <IS name>_user_manage
      example: crux_user_manage
      example: all_user_manage

    Users:
      Keycloak is supposed to has a User Federation (LDAP catalog, AD)
      Users are being found by username.
    """

    suffix = 'manage'

    def __init__(self, config, verify):
        """
        Create Keycloak Instance.

        Some info about some attributes:
        client_secret_key:
            Client secret credencials.
            For each 'access type':
                - bearer-only -> Optional
                - public -> Mandatory
                - confidencial -> Mandatory

        Returns:
            object: Keycloak object
        """
        self.config = config

        try:
            self.server_url = self.config['KEYCLOAK_SERVER_URL']
            self.realm = self.config['KEYCLOAK_REALM']
            self.client_id = self.config['KEYCLOAK_CLIENT_ID']
            self.client_secret_key = self.config['KEYCLOAK_CLIENT_SECRET_KEY']
            self.tech_user = self.config['KEYCLOAK_TECH_USER']
            self.tech_password = self.config['KEYCLOAK_TECH_PASSWORD']
        except KeyError:
            raise KeycloakException("The mandatory KEYCLOAK configuration variables has not defined.")

        if any(param is None for param in [self.server_url,
                                           self.realm,
                                           self.client_id,
                                           self.client_secret_key,
                                           self.tech_user,
                                           self.tech_password]):
            raise KeycloakException("At least one of the mandatory KEYCLOAK configuration variables is None.")

        self.client_uuid = ''
        self.token = ''
        self.refresh_token = ''
        self.token_expiration = 0
        self.refresh_token_expiration = 0

        self.auth_headers = {"Content-type": "application/x-www-form-urlencoded"}
        self.auth_data = {
            "username": self.tech_user,
            "password": self.tech_password,
            "client_id": "admin-cli",
            "scope": "openid",
            "grant_type": "password"
        }
        self.auth_refresh_data = {
            "client_id": "admin-cli",
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        self.verify = verify
        if not self.verify:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.session = requests.Session()
        self.headers = {"Content-type": "application/json", "Authorization": f"Bearer {self.token}"}

        # Endpoints for user/group management
        self.token_endpoint = f"/realms/{self.realm}/protocol/openid-connect/token"
        self.clients_endpoint = f"/admin/realms/{self.realm}/clients"
        self.users_endpoint = f"/admin/realms/{self.realm}/users"
        self.groups_endpoint = f"/admin/realms/{self.realm}/groups"
        self.roles_endpoint = f"/admin/realms/{self.realm}/clients/%(client_uuid)s/roles"
        self.user_group_endpoint = f"/admin/realms/{self.realm}/users/%(user_uuid)s/groups/%(group_uuid)s"
        self.role_group_mapping_endpoint = \
            f"/admin/realms/{self.realm}/groups/%(group_uuid)s/role-mappings/clients/%(client_uuid)s"

        super(KeycloakWorker, self).__init__(server_url=self.server_url,
                                             realm_name=self.realm,
                                             client_id=self.client_id,
                                             client_secret_key=self.client_secret_key)

    def __enter__(self):
        self.get_token(auth_data=self.auth_data)
        return self

    def __exit__(self, *excinfo):
        self.session.close()

    def get_token(self, auth_data):
        try:
            resp = self.session.post(f'{self.server_url}{self.token_endpoint}',
                                     headers=self.auth_headers,
                                     data=auth_data,
                                     verify=self.verify)
            resp.raise_for_status()
            result = resp.json()

            self.token = result['access_token']
            self.refresh_token = result['refresh_token']
            self.token_expiration = time.time() + float(result['expires_in'])
            self.refresh_token_expiration = time.time() + float(result['refresh_expires_in'])
            self.headers = {"Content-type": "application/json", "Authorization": f"Bearer {self.token}"}
            self.auth_refresh_data = {"client_id": "admin-cli", "grant_type": "refresh_token",
                                      "refresh_token": self.refresh_token}
        except Exception as error:
            raise KeycloakException(f'Request for access token failed. Error: {error}')

    @token_decorator
    def get_group(self, is_code=None, name_type="hostname", group_name=None, suffix=suffix):
        groupname = group_name or f"{is_code}_{name_type}_{suffix}"
        try:
            resp = self.session.get(f'{self.server_url}{self.groups_endpoint}?search={groupname}',
                                    headers=self.headers,
                                    verify=self.verify)
            resp.raise_for_status()
            group = resp.json()
        except Exception as error:
            raise KeycloakException(f'Request for {groupname} group failed. Error: {error}')
        return group

    @token_decorator
    def get_group_members(self, is_code, name_type="hostname", suffix=suffix):
        try:
            group = self.get_group(is_code=is_code, name_type=name_type)
            if not group:
                return {'error': 'Group not found'}
            group_uuid = group[0]['id']

            resp = requests.get(url=f"{self.server_url}{self.groups_endpoint}/{group_uuid}/members",
                                headers=self.headers,
                                verify=self.verify)
            resp.raise_for_status()
            members = resp.json()
        except Exception as error:
            raise KeycloakException(
                f'Request for {is_code}_{name_type}_{suffix} group members failed. Error: {error}')
        return members

    @token_decorator
    def get_user(self, username):
        try:
            resp = self.session.get(f'{self.server_url}{self.users_endpoint}?search={username}',
                                    headers=self.headers,
                                    verify=self.verify)
            resp.raise_for_status()
            user = resp.json()
        except Exception as error:
            raise KeycloakException(f'Request for {username} user failed. Error: {error}')
        return user

    @token_decorator
    def add_user_to_group(self, is_code, username, name_type="hostname", suffix=suffix):
        try:
            user = self.get_user(username=username)
            if not user:
                return {'error': 'User not found'}
            user_uuid = user[0]['id']

            group = self.get_group(is_code=is_code, name_type=name_type)
            if not group:
                return {'error': 'Group not found'}
            group_uuid = group[0]['id']

            endpoint = self.user_group_endpoint % {'user_uuid': user_uuid, 'group_uuid': group_uuid}
            resp = self.session.put(f'{self.server_url}{endpoint}',
                                    headers=self.headers,
                                    verify=self.verify)
            resp.raise_for_status()
        except Exception as error:
            raise KeycloakException(
                f'Request for adding {username} user to {is_code}_{name_type}_{suffix} group failed. '
                f'Error: {error}')
        return {'success': True}

    @token_decorator
    def remove_user_from_group(self, is_code, username, name_type="hostname", suffix=suffix):
        try:
            user = self.get_user(username=username)
            if not user:
                return {'error': 'User not found'}
            user_uuid = user[0]['id']

            group = self.get_group(is_code=is_code, name_type=name_type)
            if not group:
                return {'error': 'Group not found'}
            group_uuid = group[0]['id']

            endpoint = self.user_group_endpoint % {'user_uuid': user_uuid, 'group_uuid': group_uuid}
            resp = self.session.delete(f'{self.server_url}{endpoint}',
                                       headers=self.headers,
                                       verify=self.verify)
            resp.raise_for_status()
        except Exception as error:
            raise KeycloakException(f'Request for removing {username} user '
                                    f'from {is_code}_{name_type}_{suffix} group failed. Error: {error}')
        return {'success': True}

    @token_decorator
    def get_client_uuid(self):
        try:
            resp = requests.get(url=f"{self.server_url}{self.clients_endpoint}?clientId={self.client_id}",
                                headers=self.headers,
                                verify=self.verify)
            resp.raise_for_status()
            self.client_uuid = resp.json()[0].get('id')
        except Exception as error:
            raise KeycloakException(f'Request for {self.client_id} client failed. Error: {error}')
        return self.client_uuid

    @token_decorator
    def get_role(self, role_name=None, is_code=None, name_type=None, suffix=suffix):
        rolename = role_name or f"{is_code}:{name_type}:{suffix}"
        client_uuid = self.client_uuid or self.get_client_uuid()
        endpoint = self.roles_endpoint % {'client_uuid': client_uuid}
        try:
            resp = requests.get(url=f"{self.server_url}{endpoint}?search={rolename}",
                                headers=self.headers,
                                verify=self.verify)
            resp.raise_for_status()
            role = resp.json()
        except Exception as error:
            raise KeycloakException(f'Request for {rolename} role failed. Error: {error}')
        return role

    @token_decorator
    def create_role(self, is_code, name_type, suffix=suffix):
        rolename = f"{is_code}:{name_type}:{suffix}"
        client_uuid = self.client_uuid or self.get_client_uuid()
        endpoint = self.roles_endpoint % {'client_uuid': client_uuid}
        if (roles := self.get_role(role_name=rolename)) and [rls for rls in roles if rls.get('name') == rolename]:
            return
        try:
            resp = self.session.post(f'{self.server_url}{endpoint}',
                                     json={"name": rolename},
                                     headers=self.headers,
                                     verify=self.verify)
            resp.raise_for_status()
        except Exception as error:
            raise KeycloakException(f'Request for creating {rolename} role failed. Error: {error}')

    @token_decorator
    def create_group(self, is_code, name_type, suffix=suffix):
        groupname = f"{is_code}_{name_type}_{suffix}"
        if (groups := self.get_group(group_name=groupname)) and [grp for grp in groups if grp.get('name') == groupname]:
            return
        try:
            resp = self.session.post(f'{self.server_url}{self.groups_endpoint}',
                                     json={"name": groupname},
                                     headers=self.headers,
                                     verify=self.verify)
            resp.raise_for_status()
        except Exception as error:
            raise KeycloakException(f'Request for creating {groupname} group failed. Error: {error}')

    @token_decorator
    def create_role_mapping(self, role=None, group=None, is_code=None, name_type=None, suffix=suffix):
        if not group:
            groupname = f"{is_code}_{name_type}_{suffix}"
            group = [grp for grp in self.get_group(group_name=groupname) if grp.get('name') == groupname]

        group_uuid = group[0]['id']
        client_uuid = self.client_uuid or self.get_client_uuid()
        endpoint = self.role_group_mapping_endpoint % {'client_uuid': client_uuid, 'group_uuid': group_uuid}

        if not role:
            rolename = f"{is_code}:{name_type}:{suffix}"
            role = [rl for rl in self.get_role(role_name=rolename) if rl.get('name') == rolename]

        try:
            resp = self.session.post(f'{self.server_url}{endpoint}',
                                     json=role,
                                     headers=self.headers,
                                     verify=self.verify)
            resp.raise_for_status()
        except Exception as error:
            raise \
                KeycloakException(f'Request for creating {role} {group_uuid} role-group mapping failed. Error: {error}')
        return {'success': True}

    def well_known(self):
        """Lists endpoints and other configuration options
        relevant to the OpenID Connect implementation in Keycloak.

        Returns:
            [type]: [list of keycloak endpoints]
        """
        response = requests.request("GET", self.well_known_endpoint, verify=self.verify)
        return response.json()

    def introspect(self, token, token_type_hint=None):
        """
        Introspection Request token
        Implementation: https://tools.ietf.org/html/rfc7662#section-2.1

        Args:
            token (string):
                REQUIRED. The string value of the token.  For access tokens, this
                is the "access_token" value returned from the token endpoint
                defined in OAuth 2.0 [RFC6749], Section 5.1.  For refresh tokens,
                this is the "refresh_token" value returned from the token endpoint
                as defined in OAuth 2.0 [RFC6749], Section 5.1.  Other token types
                are outside the scope of this specification.
            token_type_hint ([string], optional):
                OPTIONAL.  A hint about the type of the token submitted for
                introspection.  The protected resource MAY pass this parameter to
                help the authorization server optimize the token lookup.  If the
                server is unable to locate the token using the given hint, it MUST
                extend its search across all of its supported token types.  An
                authorization server MAY ignore this parameter, particularly if it
                is able to detect the token type automatically.  Values for this
                field are defined in the "OAuth Token Type Hints" registry defined
                in OAuth Token Revocation [RFC7009].

        Returns:
            json: The introspect token
        """
        payload = {
            "token": token,
            "client_id": self.client_id,
            "client_secret": self.client_secret_key
        }
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Bearer " + token
        }

        response = requests.request("POST", self.token_introspection_endpoint, data=payload,
                                    headers=headers, verify=self.verify)
        return response.json()

    def userinfo(self, token):
        """Get user info from authenticated token

        Args:
            token (str): The string value of the token.

        Returns:
            json: user info data
        """
        headers = {
            'authorization': "Bearer " + token
        }
        response = requests.request("GET", self.userinfo_endpoint, headers=headers, verify=self.verify)
        return response.json()
