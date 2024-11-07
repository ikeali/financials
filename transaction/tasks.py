
from celery import shared_task
from django.core.mail import send_mail
from .models import *
from decouple import config

# @shared_task
# def check_transaction_limit(user_id, amount):
#     #  check if the user has sufficient balance or meets the limit criteria
#     user = User.objects.get(id=user_id)
#     if user.balance < amount:
#         send_mail(
#             'Transaction Limit Exceeded',
#             f'Dear {user.username}, your transaction of amount {amount} exceeds your limit.',
#             config('EMAIL_HOST_USER'),
#             [user.email],
#             fail_silently=False,
#         )




@shared_task
def check_transaction_limit(user_id, amount):
    try:
        user = User.objects.get(id=user_id)
        account = Account.objects.get(user=user)  
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
        return "User not found"
    except Account.DoesNotExist:
        print(f"Account for user {user_id} does not exist.")
        return "Account not found"

    # Check if the transaction amount exceeds the account balance
    if account.balance < amount:
       print('sending')
       send_mail(
            'Transaction Limit Exceeded',
            f'Dear {user.username}, your transaction of amount {amount} exceeds your limit.',
            config('EMAIL_HOST_USER'),
            [user.email],
            fail_silently=False,
        )



@shared_task
def send_email_notification(email, subject, message):
    send_mail(
        subject,
        message,
        config('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )



