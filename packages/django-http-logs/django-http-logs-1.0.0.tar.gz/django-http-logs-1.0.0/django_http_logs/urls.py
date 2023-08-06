"""
Author:     LanHao
Date:       2020/11/16
Python:     python3.6

"""

from django.urls import path,re_path,include
from rest_framework import routers
from . import views

urlpatterns = [
    path(r"apis/",views.LogsRestfulAPI.as_view({"get": "list", "post": "create"}),name="log_apis"),
]