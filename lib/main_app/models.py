from django.db import models
from account.models import CustomUser


class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя", null=False)
    slug = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, verbose_name="Фамилия", null=False)
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", null=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True)
    description = models.TextField(verbose_name="Описание", null=True)
    photo = models.ImageField(upload_to="authors/photos", null=True, blank=True)


class Book(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", null=False)
    slug = models.CharField(max_length=100, null=False)
    description = models.TextField(verbose_name="Описание", null=True)
    pages = models.IntegerField(verbose_name="Количество страниц", null=False)
    cost = models.FloatField(verbose_name="Цена", null=False)
    cover = models.ImageField(upload_to="books/covers", null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=False)


class Instance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=False)
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")


class Rent(models.Model):
    user_email = models.ForeignKey(CustomUser, models.CASCADE, null=False)
    instance_id = models.ForeignKey("Instance", models.CASCADE, null=False)
    start_date = models.DateField(verbose_name="Дата начала", null=False)
    end_date = models.DateField(verbose_name="Дата окончания", null=False)
    actual_end_date = models.DateField(verbose_name="Дата сдачи", null=True)
    cost = models.FloatField(verbose_name="Индексация", null=True)
