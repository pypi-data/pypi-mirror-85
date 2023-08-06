from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from integration_utils.mixins import CredentialMixin
from integration_utils.views import BaseCredentialModelViewSet, BaseReportListAPIView

from .models import Credential
from .serializers import CredentialSerializer


class CredentialModelViewSet(BaseCredentialModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def create(self, request, format=None):
        """must be implemented"""
        return Response({"status": "error", 'message': "IMPLEMENT ME"}, status=422)
