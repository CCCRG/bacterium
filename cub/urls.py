from django.urls import path, re_path
from cub import requests_functions

urlpatterns = [
    path("", requests_functions.hello, name="cub"),
    re_path(r'^json/$', requests_functions.json_1),
    re_path(r'^start/$', requests_functions.start),
    re_path(r'^stop/$', requests_functions.stop),
    re_path(r'^get_foods/$', requests_functions.get_div_foods),
    re_path(r'^add_food/$', requests_functions.add_food),
    re_path(r'^del_food/$', requests_functions.del_food),
]