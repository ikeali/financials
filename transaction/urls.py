from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('create_transactions/', TransactionCreateAPIView.as_view(), name='create-transaction'),
    path('see_transactions/', TransactionListAPIView.as_view(), name='see-transactions'),
    path('admin/transactions/', AdminTransactionListAPIView.as_view(), name='admin-transaction-list'),

]

