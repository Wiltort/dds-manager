import datetime
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category})"

class Transaction(models.Model):
    created_at = models.DateField(default=datetime.date.today(), verbose_name='Дата создания')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT, verbose_name='Тип')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name='Подкатегория')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Сумма')
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.created_at} - {self.amount} - {self.category}"

