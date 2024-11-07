from rest_framework import generics,status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .tasks import check_transaction_limit  # Assuming your Celery task is in tasks.py



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransactionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account = Account.objects.get(user=request.user)
            transaction_type = serializer.validated_data.get("transaction_type")
            amount = serializer.validated_data.get("amount")
            transaction = serializer.save(user=request.user)

            # Initialize status to 'pending'
            transaction.status = "pending"

            # Limit check for withdrawals and transfers
            if transaction_type in ["withdrawal", "transfer"]:
                if account.balance < amount:
                    # Trigger asynchronous email if the limit is exceeded
                    check_transaction_limit.delay(request.user.id, amount)

                    transaction.status = "failed"
                    transaction.save()
                    return Response(
                        {'error': 'Transaction exceeds your allowed balance limit.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Handle different transaction types
            if transaction_type == "deposit":
                account.update_balance(amount)
                transaction.status = "completed"
            elif transaction_type == "withdrawal":
                if account.balance >= amount:
                    account.update_balance(-amount)
                    transaction.status = "completed"
                else:
                    transaction.status = "failed"
            elif transaction_type == "transfer":
                recipient_account_number = request.data.get("recipient_account_number")
                recipient_bank_name = request.data.get("recipient_bank_name")

                if not recipient_account_number or not recipient_bank_name:
                    transaction.status = "failed"
                    transaction.save()
                    return Response(
                        {'error': 'Recipient account number and bank name are required for transfers.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    recipient_account = Account.objects.get(
                        account_number=recipient_account_number,
                        bank_name=recipient_bank_name
                    )
                    if account.balance >= amount:
                        account.update_balance(-amount)
                        recipient_account.update_balance(amount)
                        transaction.status = "completed"
                    else:
                        transaction.status = "failed"
                except Account.DoesNotExist:
                    transaction.status = "failed"
                    transaction.save()
                    return Response(
                        {'error': 'Recipient account does not exist.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            transaction.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TransactionListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
        transactions = Transaction.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    


class AdminTransactionListAPIView(APIView):
    """
    Admin-only view to list all transactions.
    """
    # Require authentication and admin permissions
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to view this data."}, status=403)

        # Query all transactions
        transactions = Transaction.objects.all()
        
        # Paginate the results
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(transactions, request)
        
        serializer = TransactionSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)


