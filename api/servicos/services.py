from datetime import date

from decouple import config

from core.firebird import FirebirdConnector
from servicos.models import OrdemServico, OrdemServicoItem, Servico
from servicos.serializers import OrdemServicoItemSerializer


class OrdemServicoService:
    def __init__(self, os: OrdemServico):
        self.os = os

    def integrar_hifuzion(self):
        conn_str = config('FIREBIRD_URL')
        conn = FirebirdConnector(connection=conn_str)

        sql_venda = '''
            insert into venda_integracao (
              id,
              filial_id,
              data,
              forma_pagamento_id,
              cliente_id
            ) values (
              ?,
              ?,
              ?,
              ?,
              ?
            ) returning id      
        '''

        sql_venda_itens = '''
            insert into venda_integracao_item (
              venda_integracao_id,
              produto_id,
              quantidade,
              unitario,
              descricao
            ) values (
              ?,
              ?,
              ?,
              ?,
              ?
            )            
        '''

        id_venda = conn.next('gen_venda_integracao_id')

        data_venda = (
            id_venda,
            1,
            date.today() if self.os.data_encerramento is None else self.os.data_encerramento,
            1,
            self.os.cliente.codigo_cliente,
        )

        conn.execute(sql_venda, data_venda, auto_commit=False)

        for i in self.os.ordemservicoitem_set.all():
            data_venda_item = (
                id_venda,
                i.servico.codigo_erp,
                1,
                i.valor,
                i.descricao
            )

            conn.execute(sql_venda_itens, data_venda_item, auto_commit=False)

        conn.commit()

    def preparar_finalizacao(self, user):
        tecnicos = [dict(tecnico=t.tecnico.nome,
                         tipo=t.tipo.descricao,
                         valor=t.valor,
                         tempo=t.tempo) for t in self.os.ordemservicotecnico_set.all()]
        servico = Servico.objects.all().first()

        trabalhos = [f'{t.get("tipo")} por {t.get("tecnico")} durante {t.get("tempo")} hora(s)' for t in tecnicos]
        texto = ', '.join(trabalhos)
        texto[0].upper() + texto[1:]

        return dict(
            ordem_servico=self.os.pk,
            desconto=self.os.desconto,
            data_encerramento=date.today(),
            servico=servico.pk,
            valor=sum([v.get('valor', 0) for v in tecnicos]),
            tempo=sum([v.get('tempo', 0) for v in tecnicos]),
            descricao=texto,
            gerar_integracao=self.os.gerar_integracao
        )

    def finalizar(self, data):
        desconto = data.pop('desconto', 0)
        gerar_integracao = data.pop('gerar_integracao', True)
        serializer = OrdemServicoItemSerializer(data=data)
        if not serializer.is_valid():
            raise Exception('Falha na serialização da finalização')

        serializer.save()
        self.os.status = OrdemServico.FINALIZADA
        self.os.desconto = desconto
        self.os.gerar_integracao = gerar_integracao
        self.os.save()

        if self.os.gerar_integracao:
            self.integrar_hifuzion()

    def cancelar(self, data):
        self.os.motivo_cancelamento = data.get('motivo_cancelamento', '')
        self.os.data_cancelamento = date.today()
        self.os.usuario_cancelamento_id = data.get('usuario', None)
        self.os.status = OrdemServico.CANCELADA
        self.os.save()
