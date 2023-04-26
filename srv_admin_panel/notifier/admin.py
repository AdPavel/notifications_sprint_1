from django.contrib import admin
from .models import Channel, Content, Template, User, Notification
import smtplib
from email.message import EmailMessage
from django.template import loader
import os


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_subscribed', 'is_confirmed')
    search_fields = ('first_name', 'last_name', 'email', 'id')
    list_filter = ('is_subscribed', 'is_confirmed')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file',)
    search_fields = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'priority', 'status', 'created_at', 'modified_at')
    list_filter = ('channel', 'priority', 'status')
    filter_horizontal = ('recipients',)
    autocomplete_fields = ('content', 'template', 'channel')
    actions = ('send',)

    @admin.action(description="Отправить")
    def send(self, request, queryset):

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        sender_email = os.getenv('EMAIL')
        server.login(sender_email, os.getenv('EMAIL_PASSWORD'))

        for notification in queryset:
            recipients = [user.email for user in notification.recipients.all()]

            message = EmailMessage()
            message['From'] = sender_email
            message["To"] = ",".join(recipients)
            message["Subject"] = 'Регистрация в Movies 💛'

            template = loader.get_template(notification.template.file.name)
            context = {
                'url': notification.content.text['redirect_url'],
            }
            output = template.render(context)
            message.add_alternative(output, subtype='html')

            server.sendmail(sender_email, recipients, message.as_string())

            notification.status = 'CLOSED'
            notification.save()

        server.close()


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
