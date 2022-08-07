from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_mail(mail, confirmation_code):
    send_mail(
        'Код подтверждения для доступа в api yamdb',
        f'Ваш код: {confirmation_code}',
        f'{settings.NO_REPLY_EMAIL}',
        [mail],
        fail_silently=False,
    )
