from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    def get(self, request: Request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
