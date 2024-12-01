from django.db import models
import uuid

class User(models.Model):
    userId = models.CharField(max_length=150, primary_key=True, default=uuid.uuid4)
    role = models.CharField(max_length=150, default='')
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='')
    acc_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=150, default='')
    email = models.CharField(max_length=150, default='')
    username = models.CharField(max_length=150, default='')
    password = models.CharField(max_length=150, default='')

class Category(models.Model):
    categoryId = models.CharField(max_length=150, primary_key=True, default=uuid.uuid4)
    categoryname = models.CharField(max_length=150, default='')

class Product(models.Model):
    productId = models.CharField(max_length=150, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.CharField(max_length=2000, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sellerId = models.ForeignKey(User, on_delete=models.CASCADE, default='null')

class Cart(models.Model):
    cartId = models.CharField(max_length=150, primary_key=True, default=uuid.uuid4)
    userId =  models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class ProductImage(models.Model):
    imageId = models.CharField(max_length=150, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='')

class BoughtItem(models.Model):
    boughtItemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)