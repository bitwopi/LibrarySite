from django.test import TestCase

from .models import Book, Author


# Create your tests here.
class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author_obj = Author.objects.create(
            id=1337,
            first_name="Me",
            slug="me",
            second_name="Surname",
        )

        Book.objects.create(
            id=228,
            name="тест",
            slug="test",
            description="test description",
            pages=1337,
            cost=600.50,
            author=author_obj,
        )

    def test_name_value(self):
        book = Book.objects.get(id=228)
        self.assertEquals(book.name, "тест", "Name value isn't equals to expectations")

    def test_pages_value(self):
        book = Book.objects.get(id=228)
        self.assertEquals(book.pages, 1337, "Pages value isn't equals to expectations")

    def test_absolute_url_method(self):
        book = Book.objects.get(id=228)
        self.assertEquals(book.get_absolute_url(), "/books/test/", "get_absolute_url method work wrong")
