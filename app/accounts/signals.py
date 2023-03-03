from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from libs.utils.email import Email, send_email


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    uri = "/redefinir-senha"
    key = reset_password_token.key
    absolute = instance.request.build_absolute_uri(uri)
    reset_password_url = f"{absolute}?token={key}"

    message = "Olá, \n"
    message += "Você pediu para redefinir sua senha, para fazê-lo basta clicar no link abaixo: \n"
    message += reset_password_url + " \n\n"
    message += "Caso não tenha sido você que selecionou essa opção, por favor ignore este email.\n"

    send_email(
        Email(
            subject="Redefinir senha para Querido Diário.",
            email_to=[reset_password_token.user.email],
            message=message,
        )
    )
