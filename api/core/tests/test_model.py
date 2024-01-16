from core.tests.factories import AtendenteFactory, ClienteFactory
from django.test import TestCase


class AtendenteTest(TestCase):
    def setUp(self) -> None:
        self.atendente = AtendenteFactory.create()

    def test_representation(self):
        self.assertEqual(str(self.atendente), self.atendente.name)

    def test_user_is_create(self):
        self.assertIsNotNone(self.atendente.usuario_acesso)


class ClienteTest(TestCase):
    def setUp(self) -> None:
        self.cliente = ClienteFactory.create()

    def test_representation(self):
        self.assertEqual(
            str(self.cliente), f"{self.cliente.codigo_cliente}-{self.cliente.name}"
        )

    def test_user_is_create(self):
        self.assertIsNotNone(self.cliente.usuario_acesso)
