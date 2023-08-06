"""
Django backend querying ETNA APIs for authentication.

User existence and registration is based on the API result.
"""
from django.contrib.auth.models import User
from etnawrapper import EtnaWrapper


class EtnaAuthBackend:
    """Authenticate through the ETNA API."""

    # pylint: disable=no-self-use,unused-argument
    def authenticate(self, request, username=None, password=None):
        """Make a request to the API and check for the return code."""
        client = EtnaWrapper(login=username, password=password)
        try:
            infos = client.get_user_info()
            # TODO: Use proper exception handling
        except Exception as err:
            print(f'{username}: {err}')
            return None
        username = infos['login']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:  # pylint: disable=no-member
            # Create a new user. There's no need to set a password
            # because only the password from settings.py is checked.
            user = User(pk=infos['id'], username=username, email=infos['email'])
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

    def get_user(self, user_id):
        """Fetch a user based on its user_id."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:  # pylint: disable=no-member
            return None
