from django.db.models import Q

from core.firebird import FirebirdConnector
from decouple import config

from core.models import Cliente

SQL_CLIENTE = """
    SELECT
      C.ID_CLIENTE AS CODIGO_CLIENTE,
      C.RAZAO_SOCIAL AS NOME,
      COALESCE(C.EMAIL, 'sememail' || C.ID_CLIENTE || '@email.com.br') AS EMAIL,
      C.NOME AS CONTATO, 
      COALESCE(C.FONE1, C.FONE2) AS CONTATO_TELEFONE,
      C.ATIVO
    FROM
      CLIENTE C
      JOIN (
        SELECT
          CR.COD_CLIENTE AS ID
        FROM
          CONTA_RECEBER CR
        WHERE
          COALESCE(CR.CANCELADO, 0) = 0
          AND EXTRACT(YEAR FROM CR.DATA_VENCIMENTO) = EXTRACT(YEAR FROM CURRENT_DATE)
        UNION
        SELECT
          CSB.ID_CLIENTE AS ID
        FROM
          CLIENTE_SERVICOS_BASICOS CSB
      ) F ON C.ID_CLIENTE = F.ID
    ORDER BY
      3        
"""


class ClienteIntegracao:
    def __init__(self):
        self.data = []

    def _load(self):
        c = config("FIREBIRD_URL")
        conn = FirebirdConnector(connection=c)
        self.data = conn.get(SQL_CLIENTE)

    def integrar(self):
        self._load()

        for d in self.data:
            codigo = d.get('codigo_cliente', 0)
            nome = d.get('nome', '')
            d['ativo'] = True if d['ativo'] == 1 else False
            c = Cliente.objects.filter(Q(codigo_cliente=codigo) | Q(nome=nome)).first()

            if c is None:
                c = Cliente(**d)
            else:
                for i in d.keys():
                    setattr(c, i, d[i])

            c.save()

