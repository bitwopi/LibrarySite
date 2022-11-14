import os
import dotenv

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Book

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


class ShowBook(DetailView):
    model = Book
    slug_url_kwarg = "book_slug"
    context_object_name = "book"
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super(ShowBook, self).get_context_data(**kwargs)
        context['title'] = context['book']
        return context
