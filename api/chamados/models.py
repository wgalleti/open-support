from django.db import models

from core.mixins import TempoMixin, UsuarioMixin
from core.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.usuario.username, filename)


class Anexo(models.Model):
    arquivo = models.FileField(upload_to=user_directory_path)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        to='core.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    @property
    def nome(self):
        return str(self.arquivo).split('/')[-1]

    def __str__(self):
        return f'{self.pk}'


class Ticket(TempoMixin, UsuarioMixin):
    # STATUS
    INICIADO = 'INICIADO'
    ESTAMOS_TRABALHANDO = 'ESTAMOS_TRABALHANDO'
    PRECISAMOS_INFORMACOES = 'PRECISAMOS_INFORMACOES'
    AGUARDANDO_CLIENTE = 'AGUARDANDO_CLIENTE'
    PROXIMA_VERSAO = 'PROXIMA_VERSAO'
    RESOLVIDO = 'RESOLVIDO'
    FINALIZADO = 'FINALIZADO'

    # DEPARTAMENTOS
    SUPORTE = 'SUPORTE'
    COMERCIAL = 'COMERCIAL'
    DESENVOLVIMENTO = 'DESENVOLVIMENTO'
    FINANCEIRO = 'FINANCEIRO'

    # Prioridade
    NORMAL = 'NORMAL'
    ALTA = 'ALTA'

    STATUS = (
        (INICIADO, 'Iniciado'),
        (ESTAMOS_TRABALHANDO, 'Estamos trabalhando'),
        (PRECISAMOS_INFORMACOES, 'Precisamos de informações'),
        (AGUARDANDO_CLIENTE, 'Aguardando Cliente'),
        (PROXIMA_VERSAO, 'Sairá na proxima versão'),
        (RESOLVIDO, 'Resolvido pelo Atendente'),
        (FINALIZADO, 'Finalizado'),
    )

    DEPARTAMENTOS = (
        (SUPORTE, 'Suporte'),
        (COMERCIAL, 'Comercial'),
        (DESENVOLVIMENTO, 'Desenvolvimento'),
        (FINANCEIRO, 'Financeiro'),
    )

    PRIORIDADES = (
        (NORMAL, 'Normal'),
        (ALTA, 'Urgente'),
    )
    cliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE)

    inicio = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    termino = models.DateTimeField(null=True, blank=True)
    prioridade = models.CharField(max_length=50, choices=PRIORIDADES, default=NORMAL)
    atendente = models.ForeignKey('core.Atendente', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default=INICIADO)
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS, default=SUPORTE)
    arquivos = models.ManyToManyField(
        to='chamados.Anexo',
        blank=True
    )
    versao = models.CharField(max_length=50, null=True, blank=True)
    nivel = models.IntegerField(default=User.NIVEL1, choices=User.NIVEIS)
    os = models.ForeignKey('servicos.OrdemServico', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'


class TicketInteracao(TempoMixin, UsuarioMixin):
    ticket = models.ForeignKey('chamados.Ticket', on_delete=models.CASCADE)
    atendente = models.ForeignKey('core.Atendente', on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    descricao = models.TextField()
    interno = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=Ticket.STATUS, default=Ticket.ESTAMOS_TRABALHANDO)
    departamento = models.CharField(max_length=50, choices=Ticket.DEPARTAMENTOS, default=Ticket.SUPORTE)
    arquivos = models.ManyToManyField(
        to='chamados.Anexo',
        blank=True
    )

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'interação'
        verbose_name_plural = 'interações'
        ordering = ('id',)
