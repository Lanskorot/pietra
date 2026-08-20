from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )
    image = models.ImageField(upload_to='category_img/', null=True, blank= True, verbose_name='Изображение')
    icon = models.FileField(upload_to='category_icon/', null=True, blank=True, verbose_name='Иконка (SVG)')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name)
            if not self.slug:
                import time
                self.slug = f"cat-{int(time.time())}-{hash(self.name)}"
        super().save(*args, **kwargs)


class Attribute(models.Model):
    """Модель для определения характеристик товаров"""
    TYPE_CHOICES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('boolean', 'Да/Нет'),
        ('select', 'Выбор из списка'),
        ('multiselect', 'Множественный выбор'),
        ('date', 'Дата'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название атрибута")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='text', verbose_name="Тип данных")
    # Для select/multiselect храним варианты в JSON-списке
    options = models.JSONField(default=list, blank=True, verbose_name="Варианты выбора")
    # Категории, к которым применяется атрибут (если не указано, то глобальный)
    categories = models.ManyToManyField(
        Category,
        related_name='attributes',
        blank=True,
        verbose_name="Категории (к каким относится)"
    )
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Единица измерения")
    is_filterable = models.BooleanField(default=True, verbose_name="Доступен для фильтрации")
    is_required = models.BooleanField(default=False, verbose_name="Обязательный")

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Рейтинг")
    image = models.ImageField(upload_to='product_img/', null=True, blank= True, verbose_name='Изображение')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name="Категория"
    )
    # Храним дополнительные атрибуты как JSON (для быстрого доступа и кеширования)
    # А также для фильтрации используем отдельную модель ProductAttributeValue (ниже)
    attributes_cache = models.JSONField(default=dict, blank=True, verbose_name="Кеш атрибутов (JSON)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_attribute_value(self, attribute_slug):
        """Получить значение атрибута по слагу"""
        try:
            return self.attribute_values.get(attribute__slug=attribute_slug).get_value_display()
        except ProductAttributeValue.DoesNotExist:
            return None


class ProductAttributeValue(models.Model):
    """Значения атрибутов для конкретного товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    # Для разных типов используем разные поля
    value_text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Текстовое значение")
    value_number = models.FloatField(blank=True, null=True, verbose_name="Числовое значение")
    value_boolean = models.BooleanField(default=False, verbose_name="Булево значение")
    value_date = models.DateField(blank=True, null=True, verbose_name="Дата")

    class Meta:
        unique_together = ('product', 'attribute')
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"
        indexes = [
            models.Index(fields=['attribute', 'value_text']),
            models.Index(fields=['attribute', 'value_number']),
            models.Index(fields=['attribute', 'value_boolean']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.get_value_display()}"

    def get_value_display(self):
        attr_type = self.attribute.type
        if attr_type == 'number':
            return str(self.value_number) if self.value_number is not None else ''
        if attr_type == 'boolean':
            return 'Да' if self.value_boolean else 'Нет'
        if attr_type == 'date':
            return self.value_date.strftime('%d.%m.%Y') if self.value_date else ''
        return self.value_text or ''

    def set_value(self, value):
        """Установить значение в зависимости от типа атрибута"""
        attr_type = self.attribute.type
        if attr_type == 'number':
            self.value_number = float(value)
        elif attr_type == 'boolean':
            self.value_boolean = bool(value)
        elif attr_type == 'date':
            self.value_date = value
        else:
            self.value_text = str(value)