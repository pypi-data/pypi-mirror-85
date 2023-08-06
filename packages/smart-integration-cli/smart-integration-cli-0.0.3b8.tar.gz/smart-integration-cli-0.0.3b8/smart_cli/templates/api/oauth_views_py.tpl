import requests
import json
import time
import datetime

from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework import status

from integration_utils.mixins import CredentialMixin
from integration_utils.views import BaseCredentialModelViewSet, BaseGetCredentialAPIView

from .models import Credential
from .serializers import CredentialSerializer


class CredentialModelViewSet(BaseCredentialModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def create(self, request, format=None):
        """must be implemented"""
        return Response({"status": "error", 'message': "IMPLEMENTED ME"}, status=403)


class GetCredentialAPIView(BaseGetCredentialAPIView):
    def get_state(self):
        """
        ---
        parameters:
            - Authorization token in headers
            - 'callback_url' in GET params
        """
        request = self.check_auth_params()
        user_info = self.get_user_info(self.request, get_token=True)
        user_id = user_info["id"]
        main_user = user_info["username"]
        # user_id = 16
        # main_user = "main_user"

        state = {
            "callback_url": request.GET['callback_url'],
            "user_id": user_id,
            "main_user": main_user,
            "platform_id": request.GET['platform_id']
        }
        return state

    def get_redirect_uri(self):
        return f"https://google.com/?state={self.get_state()}"
