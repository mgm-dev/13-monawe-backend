from django.db import models
from user.models import User, Address
from product.models import Product, ProductOption

# autopep8: off

class Order(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    address       = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_request = models.CharField(max_length=45)
    date          = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'orders'

class Status(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'statuses'

class OrderStatus(models.Model):
    order  = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta():
        db_table = 'order_statuses'

class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_option  = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    product_amount  = models.IntegerField()

    class Meta():
        db_table = 'order_products'

class DeliveryInfo(models.Model):
    order_product   = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    company         = models.CharField(max_length=45)
    tracking_number = models.CharField(max_length=45)

    class Meta():
        db_table = 'delivery_infos'

class ProductReview(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating     = models.DecimalField(max_digits=3, decimal_places=1)
    title      = models.CharField(max_length=45)
    content    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    image_url  = models.URLField(max_length=200, null=True)

    class Meta():
        db_table = 'product_reviews'


class WishProduct(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta():
        db_table = 'wish_products'

class ViewedProduct(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta():
        db_table = 'viewed_products'