from django.conf.urls.static import static
from django.urls import path
from .views import MainPageView, BooksCatalog, ShowBook, ShowGenre
from lib import settings

urlpatterns = [
    path('', MainPageView.as_view(), name="home"),
    path('book_catalog/', BooksCatalog.as_view(), name="book-catalog"),
    path('books/<slug:book_slug>/', ShowBook.as_view(), name="book"),
    path('author/<slug:author_slug>/', MainPageView.as_view(), name="author"),
    path('genre/<slug:genre_slug>/', ShowGenre.as_view(), name="genre"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
