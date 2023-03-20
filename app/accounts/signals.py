from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from libs.utils.email import Email, send_email


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    key = reset_password_token.key
    reset_password_url = (
        f"{settings.FRONT_BASE_URL}/educacao/redefinir-senha?token={key}"
    )

    message = "Olá, \n"
    message += "Você pediu para redefinir sua senha, para fazê-lo basta clicar no link abaixo: \n"
    message += reset_password_url + " \n\n"
    message += "Caso não tenha selecionado essa opção, por favor, ignore este e-mail.\n"

    send_email(
        Email(
            subject="Querido Diário - Redefinição de senha",
            email_to=[reset_password_token.user.email],
            message=message,
        )
    )
