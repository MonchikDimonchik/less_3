from django.db import models
from django.contrib.auth.models import User


# Категория товаров
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


# Товар
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="Изображение товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


# Профиль пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


# Заказ
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Общая сумма заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%Y-%m-%d')}"


# Промежуточная модель для связи многие ко многим между Заказом и Товаром
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"