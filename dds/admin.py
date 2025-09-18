from django.contrib import admin
from dds.models import Status, TransactionType, Category, SubCategory, Transaction


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(TransactionType)
class TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
