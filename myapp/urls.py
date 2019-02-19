from django.conf.urls import url, include
import myapp.views as views

urlpatterns = [
url(r'init_book$', views.init_book, ),
url(r'upload_file$', views.upload_file, ),
]
