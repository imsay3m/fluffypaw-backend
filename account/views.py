from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserAccount
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserAccountSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # print(user)
            token = default_token_generator.make_token(user)
            print("Token: " + str(token))
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("UID: " + str(uid))
            domain = get_current_site(self.request).domain
            confirm_link = f"https://{domain}/user/activate/{uid}/{token}"
            email_subject = "Confirm Your Account"
            email_body = render_to_string(
                "account/confirmation_mail.html", {"confirm_link": confirm_link}
            )
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check Your Mail For Confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return redirect("register")


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "user_id": user.id})
            else:
                return Response({"error": "Invalid Credential"})
        return Response(serializer.errors)


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    # permission_classes = IsAuthenticated
    serializer_class = UserUpdateSerializer


class ChangePasswordView(UpdateAPIView):

    queryset = User.objects.all()
    # permission_classes = IsAuthenticated
    serializer_class = ChangePasswordSerializer


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, "auth_token") and request.user.auth_token:
            request.user.auth_token.delete()
        logout(request)
        return redirect("login")
