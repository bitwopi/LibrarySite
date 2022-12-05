from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user

    def get_group_permissions(self, user_obj, obj=None):
        user_group_field = get_user_model()._meta.get_field("group")
        user_group_query = "group__%s" % user_group_field.related_query_name()
        result = Permission.objects.filter(**{user_group_query: user_obj})
        return result

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, "_perm_cache"):
            user_obj._perm_cache = self.get_group_permissions(user_obj, obj)
        return user_obj._perm_cache

    def get_user_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous or obj is not None:
            return set()
        return self.get_group_permissions(user_obj, obj)

