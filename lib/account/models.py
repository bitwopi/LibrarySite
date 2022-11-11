from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, patronymic=None, password=None):
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
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # DATABASE FIELDS
    email = models.EmailField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name="Имя", null=False)
    second_name = models.CharField(max_length=50, verbose_name="Фамилия", null=False)
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                              verbose_name="Группа")
    birth_date = models.DateField(verbose_name="Дата рождения", null=False)
    date_joined = models.DateField(auto_now_add=True, verbose_name="Дата создания аккаунта")
    avatar = models.ImageField(upload_to="users/avatars", null=True, blank=True)
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
