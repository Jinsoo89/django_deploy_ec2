from django.conf.urls import url
from . import views

app_name = 'member'
urlpatterns = [
    url(r'^sana/$', views.sana, name='sana'),
]