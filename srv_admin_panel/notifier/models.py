from django.db import models
import uuid


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class Channel(UUIDMixin):

    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Канал связи'
        verbose_name_plural = 'Каналы связи'

    def __str__(self):
        return self.name


class Content(UUIDMixin):

    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    text = models.JSONField(
        max_length=255,
        verbose_name='Содержимое'
    )

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

    def __str__(self):
        return self.name


class Template(UUIDMixin):

    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    file = models.FileField(
        upload_to='notification_templates/',
        verbose_name='Шаблон'
    )

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def __str__(self):
        return self.name


class User(UUIDMixin):

    first_name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия'
    )
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(
        default=True,
        verbose_name='Подписан на рассылку'
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name='email подтвержден'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Notification(UUIDMixin):

    recipients = models.ManyToManyField(
        to='User',
        related_name='notifications',
        verbose_name='Получатели'
    )
    content = models.ForeignKey(
        to='Content',
        null=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        verbose_name='Содержимое'
    )
    template = models.ForeignKey(
        to='Template',
        null=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        verbose_name='Шаблон'
    )
    channel = models.ForeignKey(
        to='Channel',
        null=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        verbose_name='Канал'
    )
    PRIORITIES = (
        ('LOW', 'Низкий'),
        ('MEDIUM', 'Средний'),
        ('HIGH', 'Высокий'),
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITIES,
        default='LOW',
        verbose_name='Приоритет'
    )
    STATUSES = (
        ('CREATED', 'Создан'),
        ('OPEN', 'Ждет отправки'),
        ('CLOSED', 'Отправлено'),
        ('PROCESSED', 'В процессе отправки'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='CREATED',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменения'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return str(self.id)
