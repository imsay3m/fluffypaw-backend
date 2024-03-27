from rest_framework import serializers

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

    def create(self, validated_data):
        validated_data["transaction_type"] = "Deposit"

        user = self.context["request"].user
        account = user.account

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


class AdoptPetSerializer(serializers.Serializer):
    pet_id = serializers.IntegerField()

    def validate_pet_id(self, value):
        try:
            pet = Pet.objects.get(id=value)
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Invalid pet ID.")
        if pet.adopter:
            raise serializers.ValidationError("This pet has already been adopted.")
        return value
