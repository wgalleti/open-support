from django.contrib.auth.models import AbstractUser
from django.db import models


class EmailErro(models.Model):
    data_erro = models.DateTimeField(auto_now_add=True)
    log = models.TextField()
    smtp = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.log


class User(AbstractUser):
    NIVEL1 = 1
    NIVEL2 = 2
    NIVEL3 = 3

    NIVEIS = (
        (NIVEL1, 'Suporte 1'),
        (NIVEL2, 'Suporte 2'),
        (NIVEL3, 'Suporte 3'),
    )

    is_atendente = models.BooleanField(default=False)
    is_cliente = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)
    nivel = models.IntegerField(default=NIVEL1, choices=NIVEIS)


class Atendente(models.Model):
    usuario_acesso = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    nivel = models.IntegerField(default=User.NIVEL1, choices=User.NIVEIS)
    ativo = models.BooleanField(default=True)

    valor_hora_custo = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    valor_hora_venda = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'atendente'
        verbose_name_plural = 'atendentes'


class Cliente(models.Model):
    codigo_cliente = models.IntegerField(blank=True, null=True)
    usuario_acesso = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    contato = models.CharField(max_length=100, null=True, blank=True)
    contato_telefone = models.CharField(max_length=100, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    versao = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.codigo_cliente}-{self.nome}'

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'


class ClienteAtualizacao(models.Model):
    cliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    versao = models.CharField(max_length=20)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.versao

    class Meta:
        verbose_name = 'cliente atualização'
        verbose_name_plural = 'atualizações do cliente'


class GrupoCliente(models.Model):
    nome = models.CharField(max_length=100)
    clientes = models.ManyToManyField('core.Cliente', blank=True, null=True)

    @property
    def quantidade(self):
        return len(self.clientes.all())

    def __str__(self):
        return self.nome
