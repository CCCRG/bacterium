from django.urls import path, re_path
from cub import views

urlpatterns = [
    path("", views.hello, name="cub"),
    re_path(r'^json/$', views.json_1),
    re_path(r'^start/$', views.start),
    re_path(r'^stop/$', views.stop),
    re_path(r'^get_foods/$', views.get_div_foods),
    re_path(r'^add_food/$', views.add_food),
    re_path(r'^del_food/$', views.del_food),
]