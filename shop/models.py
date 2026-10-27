from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
class Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    address_title = models.CharField(max_length=50)

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=200)

    address_line2 = models.CharField(max_length=200, blank=True)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    zip_code = models.CharField(max_length=20)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_title}"    

class Contact(models.Model): 
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Orders(models.Model):

    order_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    address = models.CharField(max_length=111)
    
    items_json = models.CharField(max_length=5000)

    name = models.CharField(max_length=90)

    email = models.CharField(max_length=111)

    city = models.CharField(max_length=111)

    state = models.CharField(max_length=111)

    zip_code = models.CharField(max_length=111)

    phone = models.CharField(max_length=111, default="")

    order_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
    ("Placed", "Placed"),
    ("Packed", "Packed"),
    ("Shipped", "Shipped"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
    ]

    status = models.CharField(
    max_length=50,
    choices=STATUS_CHOICES,
    default="Placed"
    )

    def save(self, *args, **kwargs):

      old_status = None

      if self.pk:
        old_order = Orders.objects.get(pk=self.pk)
        old_status = old_order.status

      status_changed = old_status != self.status

      super().save(*args, **kwargs)

      if status_changed:

        status_messages = {
            "Placed": "The order has been placed",
            "Packed": "Your order has been packed",
            "Shipped": "Your order has been shipped",
            "Out for Delivery": "Your order is out for delivery",
            "Delivered": "Your order has been delivered",
        }

        message = status_messages.get(self.status)

        if message:
            OrderUpdate.objects.create(
                order_id=self.order_id,
                update_desc=message
            )

    def __str__(self):
        return f"Order #{self.order_id}"

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[:20]
