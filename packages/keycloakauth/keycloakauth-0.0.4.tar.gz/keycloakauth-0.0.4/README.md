# Custom Keyclock Authentication Worker

based on Django Keycloak Auth (https://github.com/marcelo225/django-keycloak-auth) under MIT License

Class KeycloakWorker:
  - to introspect the token
  - to check if the token is active and which roles it bears
  - to get userinfo about the token owner
  - to manage Keycloak Group membership

Authentication and Authorization are based on Keycloak Roles: Role mapped to Group, User is a member of the Group.
Roles:
  - format: <IS name>:user:manage
  - example: crux:user:manage
  - example: all:user:manage

Groups:
  - format: <IS name>_user_manage
  - example: crux_user_manage
  - example: all_user_manage

Users:
  - Keycloak is supposed to has a User Federation (LDAP catalog, AD)
  - Users are being found by username


##Usage

```python
import os
from distutils.util import strtobool
from keycloakauth.keycloak import KeycloakWorker

KEYCLOAK_CONFIG = {
    'KEYCLOAK_SERVER_URL': os.getenv('KEYCLOAK_SERVER_URL', 'https://keycloak/auth'),
    'KEYCLOAK_REALM': os.getenv('KEYCLOAK_REALM', 'Master'),
    'KEYCLOAK_CLIENT_ID': os.getenv('KEYCLOAK_CLIENT_ID', 'client1'),
    'KEYCLOAK_CLIENT_SECRET_KEY': os.getenv('KEYCLOAK_CLIENT_SECRET_KEY', '12386724-1234-1234-1234-34a6214c650f'),
    'KEYCLOAK_TECH_USER': os.getenv('KEYCLOAK_TECH_USER', 'admin'),
    'KEYCLOAK_TECH_PASSWORD': os.getenv('KEYCLOAK_TECH_PASSWORD', 'admin'),
}
SSL_CRT_VERIFY = bool(strtobool(os.getenv('SSL_CRT_VERIFY', 'False')))

kworker = KeycloakWorker(config=KEYCLOAK_CONFIG, verify=SSL_CRT_VERIFY)

```