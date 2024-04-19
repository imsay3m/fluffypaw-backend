from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pet.models import Pet

from .models import Transaction
from .serializers import AdoptPetSerializer, DepositSerializer


class DepositView(APIView):
    def post(self, request):
        serializer = DepositSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            # Save the deposit transaction
            transaction = serializer.save()

            # Prepare response data
            response_data = {
                "message": "Deposit successful",
                "transaction_id": transaction.id,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" class AdoptPetAPIView(APIView):
    def post(self, request):
        serializer = AdoptPetSerializer(data=request.data)
        if serializer.is_valid():
            pet_id = serializer.validated_data["pet_id"]
            pet = Pet.objects.get(id=pet_id)
            adopting_cost = pet.price

            if request.user.account.balance < adopting_cost:
                return Response(
                    {"error": "Insufficient balance to adopt the pet."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                pet.adopter = request.user
                pet.save()

                request.user.account.balance -= adopting_cost
                request.user.account.save(update_fields=["balance"])

                Transaction.objects.create(
                    account=request.user.account,
                    amount=adopting_cost,
                    balance_after_transaction=request.user.account.balance,
                    transaction_type="Pay",
                )

            return Response(
                {"message": f"You have successfully adopted the pet: {pet.name}"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


class AdoptPetAPIView(APIView):
    def post(self, request):
        serializer = AdoptPetSerializer(data=request.data)
        if serializer.is_valid():
            adopted_pet = serializer.save()
            return Response(
                {
                    "message": f"You have successfully adopted the pet: {adopted_pet.name}"
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
