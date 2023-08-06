from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import Logs
from .serializers import LogsSerializer
from .tasks import add_log


class LogsRestfulAPI(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_log.delay(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
