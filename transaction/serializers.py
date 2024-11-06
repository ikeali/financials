from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
import random

User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

         # Generate a unique 10-digit account number
        account_number = self.generate_unique_account_number()

        # Create an Account for the user
        Account.objects.create(user=user, account_number=account_number, bank_name="Default Bank Name")

        return user

    
    def generate_unique_account_number(self):
        while True:
            account_number = str(random.randint(1000000000, 9999999999))  # 10-digit number
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance']



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'status']

    def validate_amount(self, value):
        """
        Check that the amount is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
    

    # def validate(self, data):
    #     """
    #     Additional validations for the transaction.
    #     """
    #     # Check if transaction_type is valid
    #     if data['transaction_type'] not in ['deposit', 'withdrawal', 'transfer']:
    #         raise serializers.ValidationError("Transaction type must be either deposit, withdrawal, or transfer.")
        
    #     # If the transaction type is 'withdrawal', check if sufficient funds are available
    #     if data['transaction_type'] == 'withdrawal':
    #         user_account = Account.objects.get(user=self.context['request'].user)
    #         if data['amount'] > user_account.balance:
    #             raise serializers.ValidationError("Insufficient funds for this withdrawal.")

    #     return data

    def create(self, validated_data):
        transaction_type = validated_data.get("transaction_type")
        # Set status to "completed" for deposit transactions
        if transaction_type == "deposit":
            validated_data["status"] = "completed"
        return super().create(validated_data)