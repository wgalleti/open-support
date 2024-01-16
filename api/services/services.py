from datetime import date

from decouple import config
from services.models import Service, ServiceOrder, ServiceOrderItem
from services.serializers import OrdemServicoItemSerializer


class OrdemServicoService:
    def __init__(self, os: ServiceOrder):
        self.os = os

    def preparar_finalizacao(self, user):
        tecnicos = [
            dict(
                tecnico=t.tech.name,
                tipo=t.service_type.description,
                valor=t.value,
                tempo=t.duration,
            )
            for t in self.os.ordemservicotecnico_set.all()
        ]
        servico = Service.objects.all().first()

        trabalhos = [
            f'{t.get("tipo")} por {t.get("tecnico")} durante {t.get("tempo")} hora(s)'
            for t in tecnicos
        ]
        texto = ", ".join(trabalhos)
        texto[0].upper() + texto[1:]

        return dict(
            ordem_servico=self.os.pk,
            desconto=self.os.discount,
            data_encerramento=date.today(),
            servico=servico.pk,
            valor=sum(v.get("valor", 0) for v in tecnicos),
            tempo=sum(v.get("tempo", 0) for v in tecnicos),
            descricao=texto,
            gerar_integracao=self.os.integration_create,
        )

    def finalizar(self, data):
        desconto = data.pop("desconto", 0)
        gerar_integracao = data.pop("gerar_integracao", True)
        serializer = OrdemServicoItemSerializer(data=data)
        if not serializer.is_valid():
            raise Exception("Falha na serialização da finalização")

        serializer.save()
        self.os.status = ServiceOrder.FINISHED
        self.os.discount = desconto
        self.os.integration_create = gerar_integracao
        self.os.save()

        if self.os.integration_create:
            self.integrar_hifuzion()

    def cancelar(self, data):
        self.os.cancellation_description = data.get("motivo_cancelamento", "")
        self.os.cancellation_date = date.today()
        self.os.usuario_cancelamento_id = data.get("usuario", None)
        self.os.status = ServiceOrder.CANCELED
        self.os.save()
