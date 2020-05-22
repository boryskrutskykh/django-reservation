from django.contrib import admin
from .models import Hall, Table, Order


class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height')


class TableAdmin(admin.ModelAdmin):
    list_display = (
        'hall', 'shape', 'number', 'seats', 'width', 'height', 'coordinate_x', 'coordinate_y')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('hall', 'name', 'email', 'table', 'date')


admin.site.register(Hall, HallAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
