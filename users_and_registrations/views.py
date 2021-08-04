from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_HOST_USER
from users_and_registrations.serializers import UserRegistrationSerializer, \
    ConfirmationEmailSerializer, GetJWTTokenSerializer

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            user, crated = User.objects.get_or_create(email=email)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail('User Registraion',
                      f'Hello, {email}, your code {confirmation_code}, '
                      f'your temporary password {password}',
                      EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
            return Response(status=status.HTTP_201_CREATED)


class ConfirmationEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ConfirmationEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, email=serializer.data['email'])
            if default_token_generator.check_token(user, serializer.data[
                'confirmation_code']):
                refresh = RefreshToken.for_user(user)
                user.is_active = True
                user.save()
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetJWTToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GetJWTTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            if user.check_password(serializer.data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

