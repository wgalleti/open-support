from celery import shared_task

from core.report import UsuarioReport
from core.emails import HifuzionMail
from core.models import User


@shared_task
def criar_usuario(user_id, pwd):
    user = User.objects.get(id=user_id)
    report = UsuarioReport(user, pwd)
    mail = HifuzionMail('Novo Usuário',
                        report.get_html('usuarios/novo.html'),
                        user.email)
    mail.send()

