from django.apps import AppConfig


class PerfilConfig(AppConfig):
    name = 'perfil'

    def ready(self):
        import perfil.signals
