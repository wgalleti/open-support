from django.apps import AppConfig


class ChamadosConfig(AppConfig):
    name = 'chamados'

    def ready(self):
        import chamados.signals
