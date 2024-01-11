from django.db import models

from core.mixins import TempoMixin, UsuarioMixin


class TipoServico(TempoMixin, UsuarioMixin):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'tipo serviço'
        verbose_name_plural = 'tipos de serviços'


class Servico(TempoMixin, UsuarioMixin):
    descricao = models.CharField(max_length=100)
    codigo_erp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'


class OrdemServico(TempoMixin, UsuarioMixin):
    INICIADA = 1
    EM_EXECUCAO = 2
    FINALIZADA = 3
    CANCELADA = 9

    STATUS = (
        (INICIADA, 'Iniciada'),
        (EM_EXECUCAO, 'Em Execução'),
        (FINALIZADA, 'Finalizada'),
        (CANCELADA, 'Cancelada'),
    )

    data = models.DateField()
    data_encerramento = models.DateField(null=True, blank=True)
    usuario_encerramento = models.ForeignKey('core.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='usuario_encerramento')

    data_cancelamento = models.DateField(null=True, blank=True)
    usuario_cancelamento = models.ForeignKey('core.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='usuario_cancelamento')
    motivo_cancelamento = models.TextField(null=True, blank=True)

    status = models.IntegerField(default=INICIADA, choices=STATUS)
    cliente = models.ForeignKey('core.Cliente', on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    observacoes = models.TextField(null=True, blank=True)
    desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    gerar_integracao = models.BooleanField(default=True, null=True, blank=True)

    @property
    def valor(self):
        itens = sum([i.valor for i in self.ordemservicoitem_set.all()])
        return itens - self.desconto

    @property
    def valor_previsto(self):
        itens = sum([i.valor for i in self.ordemservicotecnico_set.all()])
        return itens

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'ordem de serviço'
        verbose_name_plural = 'ordens de serviços'


class OrdemServicoItem(TempoMixin, UsuarioMixin):
    ordem_servico = models.ForeignKey('servicos.OrdemServico', on_delete=models.CASCADE)
    servico = models.ForeignKey('servicos.Servico', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    tempo = models.IntegerField(default=1, null=True, blank=True)
    descricao = models.TextField()

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'item da ordem de serviço'
        verbose_name_plural = 'itens das ordens de serviços'


class OrdemServicoTecnico(TempoMixin, UsuarioMixin):
    ordem_servico = models.ForeignKey('servicos.OrdemServico', on_delete=models.CASCADE)
    tipo = models.ForeignKey('servicos.TipoServico', on_delete=models.DO_NOTHING)
    tecnico = models.ForeignKey('core.Atendente', on_delete=models.DO_NOTHING)
    tempo = models.IntegerField()
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.pk} - {self.tecnico}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        self.ordem_servico.status = OrdemServico.EM_EXECUCAO
        self.ordem_servico.save()

    class Meta:
        verbose_name = 'técnico da ordem de serviço'
        verbose_name_plural = 'técnicos das ordens de serviços'
