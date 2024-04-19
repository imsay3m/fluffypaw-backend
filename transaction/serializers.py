from django.db import transaction
from rest_framework import serializers

from account.models import UserAccount
from pet.models import Pet

from .models import TRANSACTION_TYPE, Transaction


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["amount", "account"]
        read_only_fields = ["balance_after_transaction", "transaction_type"]

    def validate_amount(self, value):
        min_deposit_amount = 100
        if value < min_deposit_amount:
            raise serializers.ValidationError(
                f"You need to deposit at least {min_deposit_amount} $"
            )
        return value

    def validate_account(self, value):
        try:
            # Check if the UserAccount with the provided account number exists
            account = UserAccount.objects.get(id=value.id)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("Account does not exist.")
        return account

    def create(self, validated_data):
        validated_data["transaction_type"] = "Deposit"

        # user = self.context["request"].user
        # account = user.account

        account = validated_data["account"]

        current_balance = account.balance
        amount = validated_data["amount"]
        new_balance = current_balance + amount
        account.balance = new_balance
        account.save()

        # Create the transaction object
        transaction = Transaction.objects.create(
            account=account, amount=amount, balance_after_transaction=new_balance
        )

        return transaction


""" class AdoptPetSerializer(serializers.Serializer):
    pet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate_pet_id(self, value):
        try:
            pet = Pet.objects.get(id=value)
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Invalid pet ID.")
        if pet.adopter:
            raise serializers.ValidationError("This pet has already been adopted.")
        return value """


class AdoptPetSerializer(serializers.Serializer):
    pet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        pet_id = data.get("pet_id")
        user_id = data.get("user_id")

        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Invalid pet ID.")

        if pet.adopter:
            raise serializers.ValidationError("This pet has already been adopted.")

        try:
            user_account = UserAccount.objects.get(user_id=user_id)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID or account not found.")

        adopting_cost = pet.price

        if user_account.balance < adopting_cost:
            raise serializers.ValidationError("Insufficient balance to adopt the pet.")

        # Attach pet and user_account to data to use later in save method
        data["pet"] = pet
        data["user_account"] = user_account
        data["adopting_cost"] = adopting_cost

        return data

    def save(self):
        pet = self.validated_data["pet"]
        user_account = self.validated_data["user_account"]
        adopting_cost = self.validated_data["adopting_cost"]

        with transaction.atomic():
            # Update the pet's adopter
            pet.adopter_id = user_account.user_id
            pet.save()

            # Deduct adopting cost from user's balance
            user_account.balance -= adopting_cost
            user_account.save(update_fields=["balance"])

            # Create transaction record
            Transaction.objects.create(
                account=user_account,
                amount=adopting_cost,
                balance_after_transaction=user_account.balance,
                transaction_type="Pay",
            )

        return pet  # You can return the adopted pet or any other desired response
