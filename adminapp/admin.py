from django import forms
from django.contrib import admin
from django.http import HttpResponse
from userapp.models import Ticket, Category, SubCategory
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from userapp.models import Operator
import csv


class SubCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        used_letters = SubCategory.objects.values_list('letter', flat=True)
        available_letters = [(chr(i), chr(i)) for i in range(65, 91) if chr(i) not in used_letters]
        self.fields['letter'].choices = available_letters

    class Meta:
        model = SubCategory
        fields = '__all__'


@admin.action(description='Экспортировать статистику по билетам')
def export_ticket_statistics(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ticket_statistics.csv"'
    writer = csv.writer(response)
    writer.writerow(['Номер', 'Дата выпуска', 'Обслужен', 'Кем обслужен', 'Подкатегория'])

    for ticket in queryset:
        writer.writerow([
            ticket.number,
            ticket.issued_at,
            ticket.is_served,
            ticket.served_by,
            ticket.subcategory
        ])

    return response


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('number', 'issued_at', 'is_served', 'served_by', 'subcategory')
    list_filter = ('is_served', 'subcategory')
    search_fields = ('number', 'served_by')
    actions = [export_ticket_statistics]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm
    list_display = ('name', 'letter', 'category')
    search_fields = ('name',)


class OperatorInline(admin.StackedInline):
    model = Operator
    can_delete = False
    verbose_name_plural = 'operators'


class UserAdmin(BaseUserAdmin):
    inlines = (OperatorInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'window_number')
    search_fields = ('user__username', 'window_number')
