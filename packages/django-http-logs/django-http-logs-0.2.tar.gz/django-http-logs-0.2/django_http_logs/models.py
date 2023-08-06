import traceback
import logging
from datetime import datetime
from django.db import models


# Create your models here.
class Logs(models.Model):
    """
    记录日志信息,流水,除ID 外无主键
    """
    name = models.CharField(max_length=32, verbose_name="Logger Name", default="")
    msg = models.TextField(verbose_name="Msg", default="")
    args = models.TextField(verbose_name="Args", default="")

    # level
    levelname = models.CharField(max_length=8, verbose_name="Level Name", default="")
    levelno = models.CharField(max_length=32, verbose_name="Level No", default="")
    pathname = models.CharField(max_length=256, verbose_name="Path Name", default="")
    filename = models.CharField(max_length=64, verbose_name="File Name", default="")
    module = models.CharField(max_length=64, verbose_name="Module", default="")
    exc_info = models.TextField(verbose_name="Exc Info", default="")
    exc_text = models.CharField(max_length=32, verbose_name="Exc Text", default="")
    stack_info = models.CharField(max_length=32, verbose_name="Stack Info", default="")
    lineno = models.CharField(max_length=32, verbose_name="Line No", default="")
    funcname = models.CharField(max_length=32, verbose_name="Func Name", default="")

    created = models.FloatField(verbose_name="Created Timestmap", default="")
    msecs = models.FloatField(verbose_name="Msecs", default="")
    relativeCreated = models.FloatField(verbose_name="Relative Created", default="")

    thread = models.CharField(max_length=32, verbose_name="Thread", default="")
    threadName = models.CharField(max_length=32, verbose_name="Thread Name", default="")
    processName = models.CharField(max_length=32, verbose_name="Process Name", default="")
    process = models.CharField(max_length=32, verbose_name="Process", default="")

    class Meta:
        verbose_name = "日志中心"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}  {self.levelname} :{self.msg}"

    def __repr__(self):
        return self.__str__()

    def short_message(self):
        return str(self.msg)[:50]

    short_message.allow_tags = True
    short_message.short_description = "Short Message"

    def times(self):
        back: datetime = None
        try:
            back = datetime.fromtimestamp(self.created)
        except Exception:
            logging.error(traceback.format_exc())
        return back

    times.allow_tags = True
    times.short_description = "Create Times"
