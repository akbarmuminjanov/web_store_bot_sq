from django.db import models

# Create your models here.

STATUS_CHOICES=(
    ("preparing", "Tayyorlanmoqda"),
    ("delivering", "Yetkazilmoqda"),
    ("finished", "Yetkazib berildi"),
)



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="product_images/")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

class User(models.Model):
    id = models.PositiveBigIntegerField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=255)
    language = models.CharField(max_length=3, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    products = models.ManyToManyField(Product)
    total_price = models.PositiveBigIntegerField(default=0, null=True, blank=True)



    def __str__(self):
        return self.full_name
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50)

    def __str__(self):
        return f"{self.user.full_name}: {self.get_status_display()}" 
    