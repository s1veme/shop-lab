from rest_framework.generics import CreateAPIView

from api.v1.users.serializers import CreateUserSerializer
from apps.users.models import User


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
