from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import OTP
import random
import string

def send_otp_email(user):
    otp_code = OTP.generate_otp()

    # Set OTP expiration time to 5 minutes from now
    expires_at = timezone.now() + timedelta(minutes=10)

    otp_instance = OTP.objects.create(
        user=user,
        otp=otp_code,
        expires_at=expires_at
    )

    # Send OTP to the user's email
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_code}. It will expire in 5 minutes.',
        'no-reply@example.com',
        [user.email],
        fail_silently=False,
    )

    return otp_instance
