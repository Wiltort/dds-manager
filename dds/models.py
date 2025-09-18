from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class TransactionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="subcategories",
        verbose_name="Категория",
    )

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name} ({self.category})"


class Transaction(models.Model):
    created_at = models.DateField(
        default=timezone.localdate, verbose_name="Дата создания", blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        related_name="transactions",
    )
    type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name="Тип",
        related_name="transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="transactions",
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.localdate()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'dds'
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"{self.created_at} - {self.amount} - {self.category}"
