from django.db import models

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)  # Явно указанный первичный ключ
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent'],
                name='unique_category_name_per_parent'
            )
        ]
    
    def __str__(self):
        return self.full_path
    
    @property
    def full_path(self):
        """Возвращает полный путь категории"""
        if self.parent:
            return f"{self.parent} › {self.name}"
        return self.name

    def get_products(self):
        """Возвращает все товары в категории и подкатегориях"""
        from django.db.models import Q
        categories = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=categories)
    
    def get_descendants(self, include_self=False):
        """Возвращает всех потомков категории"""
        descendants = set()
        stack = [self]
        
        while stack:
            current = stack.pop()
            if include_self or current != self:
                descendants.add(current.id)
            stack.extend(current.children.all())
        
        return Category.objects.filter(id__in=descendants)

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(
        verbose_name="Полное описание",
        blank=True,
        default=""
    )
    main_image = models.ImageField(
        upload_to='products/',
        verbose_name="Основное изображение",
        blank=True,
        null=True
    )
    image1 = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение1",
        blank=True,
        null=True
    )
    image2 = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение2",
        blank=True,
        null=True
    )
    image3 = models.ImageField(
        upload_to='products/',
        verbose_name="Изображение3",
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )

    # Новые характеристики
    length = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Длина (см)",
        blank=True, null=True
    )
    width = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Ширина (см)",
        blank=True, null=True
    )
    height = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Высота (см)",
        blank=True, null=True
    )
    weight = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Вес (кг)",
        blank=True, null=True
    )
    color = models.CharField(
        max_length=50,
        verbose_name="Цвет",
        blank=True
    )
    body_material = models.CharField(
        max_length=100,
        verbose_name="Материал корпуса",
        blank=True
    )
    power = models.CharField(
        max_length=100,
        verbose_name="Мощность",
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
