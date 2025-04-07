from django.urls import path, re_path
from cub import views

urlpatterns = [
    path("", views.hello, name="cub"),
    re_path(r'^json/$', views.json_1),
    re_path(r'^insert/$', views.insert),
    re_path(r'^start/$', views.start),
    re_path(r'^stop/$', views.stop),
]