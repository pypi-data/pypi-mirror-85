from setuptools import setup, find_packages
from os import path

"""
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
"""

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='keycloakauth',
    version='0.0.4',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/VyacheslavKazakov/keycloak_auth/',
    license='MIT',
    author='Vyacheslav Kazakov',
    author_email='vyachka@gmail.com',
    description='Custom Keycloak Worker',
    install_requires=[
        'django-keycloak-auth>=0.9.1',
        'requests==2.24.0',
        'urllib3==1.25.11'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'requests-mock',
            'coverage',
            'pytest-flake8'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
