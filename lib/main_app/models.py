from django.db import models
from django.urls import reverse
from account.models import CustomUser


class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя", null=False)
    slug = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, verbose_name="Фамилия", null=False)
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True)
    photo = models.ImageField(upload_to="authors/photos", null=False)

    # META CLASS
    class Meta:
        ordering = ['second_name']
        verbose_name = "Авторы"
        verbose_name_plural = "Авторы"

    # TO STRING METHOD
    def __str__(self):
        if self.patronymic:
            return self.first_name + " " + self.second_name + " " + self.patronymic
        else:
            return self.first_name + " " + self.second_name

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    # OTHER METHODS


class Genre(models.Model):
    slug = models.CharField(max_length=25, null=False, unique=True, primary_key=True)
    name = models.CharField(max_length=25, verbose_name="Название", null=False, unique=True)

    # META CLASS
    class Meta:
        ordering = ['name']
        verbose_name = "Жанры"
        verbose_name_plural = "Жанры"

    # TO STRING METHOD
    def __str__(self):
        return self.name

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


class Book(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", null=False)
    slug = models.CharField(max_length=100, null=False)
    description = models.TextField(verbose_name="Описание", null=True)
    pages = models.IntegerField(verbose_name="Количество страниц", null=False)
    cost = models.FloatField(verbose_name="Цена", null=False)
    cover = models.ImageField(upload_to="books/covers", null=True, blank=True, verbose_name="Обложка")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name="books", null=False,
                               verbose_name="Автор")
    genres = models.ManyToManyField('Genre', related_name="books", verbose_name="Жанры")

    # META CLASS
    class Meta:
        ordering = ['name']
        verbose_name = "Книги"
        verbose_name_plural = "Книги"

    # TO STRING METHOD
    def __str__(self):
        return self.name

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    # OTHER METHODS
    def get_rent_cost(self):
        return self.cost / 20

    def get_cost(self):
        return int(self.cost)

    def get_genres(self):
        return [genre for genre in self.genres.all()]


class Instance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=False)
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")


class Rent(models.Model):
    user_email = models.ForeignKey(CustomUser, models.CASCADE, null=False)
    instance_id = models.ForeignKey("Instance", models.CASCADE, null=False)
    start_date = models.DateField(verbose_name="Дата начала", null=False)
    end_date = models.DateField(verbose_name="Дата окончания", null=False)
    actual_end_date = models.DateField(verbose_name="Дата сдачи", null=True)

