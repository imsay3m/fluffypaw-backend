from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserAccount

# from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "id",
            "user",
            "image",
            "account_no",
            "initial_deposite_date",
            "balance",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "email",
            "image",
        ]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        confirm_password = validated_data["confirm_password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        if password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken")

        user = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.is_active = False
        user.save()
        image_data = validated_data.pop("image", "images/profile/user_avatar.png")
        UserAccount.objects.create(
            user=user, image=image_data, account_no=100000 + int(user.id), balance=0
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None
            if user_account:
                self.fields["image"].initial = user_account.image

    def save(self, **kwargs):
        commit = kwargs.pop("commit", True)
        user_data = super().save(**kwargs)

        if commit:
            user_data.save()

            user_account, created = UserAccount.objects.get_or_create(user=user_data)
            user_account.image = self.validated_data.get("image", None)
            user_account.save()

        return user_data


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password fields didn't match.")

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance
