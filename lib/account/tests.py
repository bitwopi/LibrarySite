import datetime

from django.test import TestCase
from .models import CustomUser


# Create your tests here.
class TestCustomUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(
            email="test@email.ru",
            first_name="Матвей",
            second_name="Юсим",
            patronymic="Александрович",
            birth_date=datetime.datetime.now().date(),
        )

    def test_create_user_method(self):
        user = CustomUser.objects.get(email="test@email.ru")
        self.assertIsNotNone(user)

    def test_birth_date(self):
        user = CustomUser.objects.get(email="test@email.ru")
        self.assertEquals(user.birth_date, datetime.datetime.now().date(),
                          "user birth date isn't equal to expectations")

    def test_is_staff_method(self):
        user = CustomUser.objects.get(email="test@email.ru")
        self.assertFalse(user.is_staff(), "is_staff method work incorrectly")

