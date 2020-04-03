from django.conf.urls import url
from web import views

urlpatterns = [
    url('^$', views.index, name='index')
]