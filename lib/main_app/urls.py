from django.conf.urls.static import static
from django.urls import path
from .views import MainPageView, BooksCatalog
from lib import settings

urlpatterns = [
    path('', MainPageView.as_view(), name="home"),
    path('book_catalog/', BooksCatalog.as_view(), name="book-catalog"),
    path('books/<slug:book_slug>/', MainPageView.as_view(), name="book")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
