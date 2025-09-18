from django import forms
from django.contrib import admin
from dds.models import Status, TransactionType, Category, SubCategory, Transaction
from django.utils import timezone


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'transaction_count']
    search_fields = ['name']
    
    def transaction_count(self, obj):
        return obj.transactions.count()
    transaction_count.short_description = 'Кол-во транзакций'

@admin.register(TransactionType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'transaction_count']
    search_fields = ['name']
    
    def transaction_count(self, obj):
        return Transaction.objects.filter(type=obj).count()
    transaction_count.short_description = 'Кол-во транзакций'

class SubcategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ['name', 'transaction_count_display']
    readonly_fields = ['transaction_count_display']
    
    def transaction_count_display(self, obj):
        return obj.transactions.count()
    transaction_count_display.short_description = 'Транзакций'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory_count', 'transaction_count']
    search_fields = ['name']
    inlines = [SubcategoryInline]
    
    def subcategory_count(self, obj):
        return obj.subcategories.count()
    subcategory_count.short_description = 'Подкатегорий'
    
    def transaction_count(self, obj):
        return Transaction.objects.filter(category=obj).count()
    transaction_count.short_description = 'Транзакций'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'transaction_count']
    list_filter = ['category']
    search_fields = ['name', 'category__name']
    
    def transaction_count(self, obj):
        return obj.transactions.count()
    transaction_count.short_description = 'Транзакций'


class CustomDateInput(forms.DateInput):
    input_type = 'date'
    
    def format_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        # Преобразуем в формат YYYY-MM-DD для HTML5 input
        return value.strftime('%Y-%m-%d')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'created_at': CustomDateInput(
                attrs={'placeholder': 'дд.мм.гггг'}
            ),
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_at'].input_formats = [
            '%d.%m.%Y',    # 31.01.2023
            '%d.%m.%y',    # 31.01.23
            '%Y-%m-%d',    # 2023-01-31
        ]
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(
                category=self.instance.category
            )


class AmountFilter(admin.SimpleListFilter):
    title = 'Сумма'
    parameter_name = 'amount'
    
    def lookups(self, request, model_admin):
        return (
            ('small', 'Малые (< 1,000 ₽)'),
            ('medium', 'Средние (1,000-10,000 ₽)'),
            ('large', 'Крупные (> 10,000 ₽)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'small':
            return queryset.filter(amount__lt=1000)
        if self.value() == 'medium':
            return queryset.filter(amount__range=(1000, 10000))
        if self.value() == 'large':
            return queryset.filter(amount__gt=10000)
        return queryset


class DateRangeFilter(admin.SimpleListFilter):
    title = 'Диапазон дат'
    parameter_name = 'date_range'
    
    def lookups(self, request, model_admin):
        return (
            ('custom', 'Произвольный диапазон'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'custom':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            
            if start_date:
                try:
                    start_date = timezone.datetime.strptime(start_date, '%d.%m.%Y').date()
                    queryset = queryset.filter(created_at__gte=start_date)
                except ValueError:
                    pass
            
            if end_date:
                try:
                    end_date = timezone.datetime.strptime(end_date, '%d.%m.%Y').date()
                    queryset = queryset.filter(created_at__lte=end_date)
                except ValueError:
                    pass
            
            return queryset
        return queryset
    
    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string({}, [self.parameter_name, 'start_date', 'end_date']),
            'display': 'Все даты',
        }
        for lookup, title in self.lookups(None, None):
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm
    list_display = [
        'created_at_formatted', 
        'status', 
        'type', 
        'category', 
        'subcategory', 
        'amount_formatted', 
        'comment_short',
    ]
    list_filter = [
        ('created_at', admin.DateFieldListFilter),
        DateRangeFilter,
        'status',
        'type',
        'category',
        'subcategory',
        AmountFilter,
    ]
    search_fields = [
        'comment',
        'category__name',
        'subcategory__name',
        'amount'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 50
    ordering = ['-created_at']
    
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        
        # Получаем параметры фильтрации
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        
        extra_context['start_date'] = start_date
        extra_context['end_date'] = end_date
        
        return super().changelist_view(request, extra_context=extra_context)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('created_at', 'status', 'type')
        }),
        ('Детали операции', {
            'fields': ('category', 'subcategory', 'amount', 'comment')
        }),
    )

    def amount_formatted(self, obj):
        return f"{obj.amount:,.2f} ₽".replace(',', ' ')
    amount_formatted.short_description = 'Сумма'
    amount_formatted.admin_order_field = 'amount'
    
    def comment_short(self, obj):
        if obj.comment and len(obj.comment) > 50:
            return f"{obj.comment[:50]}..."
        return obj.comment or "-"
    comment_short.short_description = 'Комментарий'

    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')  # Формат 31.01.2023
    created_at_formatted.short_description = 'Дата создания'
    created_at_formatted.admin_order_field = 'created_at'

# Кастомизация заголовка админки
admin.site.site_header = 'Управление движением денежных средств (ДДС)'
admin.site.site_title = 'ДДС Админка'
admin.site.index_title = 'Панель управления'