import os
import dotenv

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Book, Genre

dotenv.load_dotenv()
PAGINATE_NUMBER = int(os.getenv('POST_NUMBER', 10))


class MainPageView(TemplateView):
    template_name = "main_app/base.html"


class BooksCatalog(ListView):
    model = Book
    paginate_by = PAGINATE_NUMBER
    template_name = "main_app/lists/book_catalog_list.html"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BooksCatalog, self).get_context_data(**kwargs)
        context['title'] = "Каталог"
        return context


class ShowGenre(ListView):
    model = Book
    paginate_by = PAGINATE_NUMBER
    template_name = "main_app/lists/books_by_category.html"
    context_object_name = "books"
    slug_url_kwarg = "genre_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowGenre, self).get_context_data(**kwargs)
        genre = Genre.objects.filter(slug=self.kwargs['genre_slug'])
        context['title'] = genre[0].name
        context['genre'] = genre[0]
        return context

    def get_queryset(self):
        return Book.objects.filter(genres__slug=self.kwargs['genre_slug'])


class ShowBook(DetailView):
    model = Book
    slug_url_kwarg = "book_slug"
    context_object_name = "book"
    template_name = "main_app/details/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ShowBook, self).get_context_data(**kwargs)
        context['title'] = context['book']
        return context
