from django.apps import AppConfig


class NotifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifier'
    verbose_name = 'Отправка уведомлений'

    def ready(self):
        import notifier.signals
