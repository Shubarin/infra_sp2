from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from ..permissions import IsAdmin
from ..serializers.users import (
    MyUserSerializer,
    UserRegistrationSerializer,
    EmailSerializer,
)

from api_yamdb.settings import EMAIL_HOST_USER


User = get_user_model()


def send_msg(email, code):
    subject = 'Response with code confirmation'
    body = f'''
        {code}
    '''
    send_mail(
        subject, body,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )


@api_view(['POST'])
def registrations_request(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, create_flag = User.objects.get_or_create(
        email=email,
        username=username,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_msg(email, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    code = serializer.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, code):
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': f'{access_token}'},
            status=status.HTTP_200_OK,
        )
    return Response(
        {'token': 'Invalid authorization token'},
        status=status.HTTP_400_BAD_REQUEST,
    )


class MyUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    search_fields = ['user__username']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
