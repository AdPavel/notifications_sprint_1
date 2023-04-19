from django.contrib import admin
from .models import Channel, Content, Template, User, Notification


admin.site.register(Channel)
admin.site.register(Content)
admin.site.register(Template)
admin.site.register(User)
admin.site.register(Notification)
