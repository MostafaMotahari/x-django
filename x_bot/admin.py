from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.XrayUser)
class XrayUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', )


@admin.register(models.XrayServer)
class XrayServerAdmin(admin.ModelAdmin):
    list_display = ('country', 'is_active', 'capacity', 'domain')


@admin.register(models.XrayService)
class XrayServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'inbound__server', 'inbound', 'price')


@admin.register(models.XrayPort)
class XrayPortAdmin(admin.ModelAdmin):
    list_display = ('xrayinbound__server', 'port_number')
