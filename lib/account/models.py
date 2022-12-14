from django.db import models
from django.utils.itercompat import is_iterable
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, _user_has_perm, \
    _user_has_module_perms


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, birth_date=None, patronymic=None, password=None):
        """
        Creates and saves a User with the given email, first name, second name, patronymic and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not second_name:
            raise ValueError('Users must have a second name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            second_name=second_name,
            patronymic=patronymic,
            birth_date=birth_date,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, second_name, birth_date=None, patronymic=None, password=None):
        """
        Creates and saves a User with the given email, first name, second name, patronymic and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not second_name:
            raise ValueError('Users must have a second name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            second_name=second_name,
            patronymic=patronymic,
            birth_date=birth_date,
            is_superuser=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # DATABASE FIELDS
    email = models.EmailField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name="??????", null=False)
    second_name = models.CharField(max_length=50, verbose_name="??????????????", null=False)
    patronymic = models.CharField(max_length=50, verbose_name="????????????????", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                              verbose_name="????????????", related_query_name="group")
    birth_date = models.DateField(verbose_name="???????? ????????????????", null=False)
    date_joined = models.DateField(auto_now_add=True, verbose_name="???????? ???????????????? ????????????????")
    avatar = models.ImageField(upload_to="users/avatars", null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=False)
    # CONSTANTS
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'second_name',
        'birth_date',
    ]

    # USER MANAGER
    objects = CustomUserManager()

    # META CLASS
    class Meta:
        ordering = ['second_name']

    # TO STRING METHOD
    def __str__(self):
        return self.email

    # OTHER METHODS
    def get_full_name(self):
        if self.patronymic:
            return self.second_name + " " + self.first_name + " " + self.patronymic
        else:
            return self.second_name + " " + self.first_name

    def is_staff(self):
        if self.is_superuser:
            return True
        elif self.group:
            if self.group.name == 'librarian':
                return True
            elif self.group.name == 'accountant':
                return True
        else:
            return False

    def has_perm(self, perm, obj=None):
        # Superusers have all permissions.
        if self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        result = all(self.has_perm(perm, obj) for perm in perm_list)
        print(result)
        return result

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)
