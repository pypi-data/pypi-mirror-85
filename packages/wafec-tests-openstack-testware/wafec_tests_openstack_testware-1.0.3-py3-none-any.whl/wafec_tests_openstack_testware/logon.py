from keystoneauth1 import identity
from keystoneauth1 import session

from .utils import get_or_env

__all__ = [
    'session_build'
]


def session_build(auth_url=None, username=None, password=None,
                  project_name=None, project_domain_name=None, user_domain_name=None):
    auth_url = get_or_env(auth_url, 'OS_AUTH_URL')
    username = get_or_env(username, 'OS_USERNAME')
    password = get_or_env(password, 'OS_PASSWORD')
    project_name = get_or_env(project_name, 'OS_PROJECT_NAME')
    project_domain_name = get_or_env(project_domain_name, 'OS_PROJECT_DOMAIN_NAME')
    user_domain_name = get_or_env(user_domain_name, 'OS_USER_DOMAIN_NAME')
    auth = identity.v3.Password(
        auth_url=auth_url,
        username=username,
        password=password,
        project_name=project_name,
        project_domain_name=project_domain_name,
        user_domain_name=user_domain_name
    )
    session_inst = session.Session(auth=auth)
    return session_inst
