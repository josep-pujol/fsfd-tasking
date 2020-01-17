from django.contrib.auth.models import User
from django.db.models import Q


class EmailAuth:
    """Authenticate user by an exact match on email and password"""

    def authenticate(self, request, username=None, password=None):
        """
        Get an instance of User using the supplied username
        or email and verify the password
        """
        try:
            # Filter all users by searching for a match by username/ email.
            users = User.objects.filter(
                Q(username__exact=username) | Q(email__exact=username)
            )

            if not users:
                return None
            user = users[0]
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Used by Django auth system to retrieve user instance"""

        try:
            user = User.objects.get(pk=user_id)

            if user.is_active:
                return user
            return None

        except User.DoesNotExist:
            return None
