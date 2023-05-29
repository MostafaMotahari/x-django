from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.XrayUser)
class XrayUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', )


@admin.register(models.XrayServer)
class XrayServerAdmin(admin.ModelAdmin):
    list_display = ('country', 'domain')


@admin.register(models.XrayInbound)
class XrayInboundAdmin(admin.ModelAdmin):
    list_display = ('server', 'capacity', 'is_active')


@admin.register(models.XrayService)
class XrayServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'price')


@admin.register(models.XrayPort)
class XrayPortAdmin(admin.ModelAdmin):
    list_display = ('port_number', )
