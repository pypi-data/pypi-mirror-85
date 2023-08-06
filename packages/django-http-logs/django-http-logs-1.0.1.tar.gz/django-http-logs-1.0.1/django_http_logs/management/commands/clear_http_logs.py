"""
Author:     LanHao
Date:       2020/11/18
Python:     python3.6

"""

from django.core.management import BaseCommand

from django_http_logs.models import Logs


class Command(BaseCommand):
    def handle(self, *args, **options):
        Logs.objects.all().delete()
