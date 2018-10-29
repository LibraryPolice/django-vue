from django.conf.urls import url, include
import myapp.views as views

urlpatterns = [
url(r'init_book$', views.init_book, ),
url(r'show_books$', views.show_books, ),
url(r'upload_file$', views.upload_file, ),
]