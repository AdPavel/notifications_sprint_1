from django.contrib import admin
from .models import Channel, Content, Template, User, Notification


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


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
