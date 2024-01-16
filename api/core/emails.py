from django.core.mail import EmailMultiAlternatives

from core.models import MailError
from support import settings


class SupportMail:

    def __init__(self, assunto, conteudo, para, html=True):
        self.conteudo = conteudo
        self.assunto = assunto
        self.from_email = 'noreply@hifuzion.com.br'
        self.to = para if isinstance(para, list) else [para]
        self.html = html

    def send(self):
        msg = EmailMultiAlternatives(self.assunto, self.conteudo, self.from_email, self.to)
        if self.html:
            msg.attach_alternative(self.conteudo, 'text/html')
        try:
            msg.send(False)
        except Exception as e:
            MailError(log=f'Classe: {e.__class__.__name__} \nErro: {str(e)}',
                      smtp=settings.EMAIL_HOST,
                      usuario=settings.EMAIL_HOST_USER,
                      senha=settings.EMAIL_HOST_PASSWORD).save()
            return False
        else:
            return True
