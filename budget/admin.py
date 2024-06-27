# expenses/admin.py

from django.contrib import admin
from .models import CustomUser, Category, Transaction,Income,CategoryIncome

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'balance']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount','date', 'description']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'description', 'date']
@admin.register(CategoryIncome)
class CategoryIncomeAdmin(admin.ModelAdmin):
    list_display = ['name']