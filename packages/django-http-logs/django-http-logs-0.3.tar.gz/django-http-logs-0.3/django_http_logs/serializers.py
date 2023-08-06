"""
Author:     LanHao
Date:       2020/11/16
Python:     python3.6

"""
from rest_framework import serializers
from .models import Logs

class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = "__all__"