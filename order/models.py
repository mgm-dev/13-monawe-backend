from django.db import models
from user.models import User, Address
from product.models import Product, ProductOption

# autopep8: off

# Order
class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'statuses'

class Order(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    address       = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    order_request = models.CharField(max_length=45, null=True)
    date          = models.DateTimeField(auto_now=True, null=True)
    order_status  = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    class Meta():

        db_table = 'orders'

class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_option  = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    product_amount  = models.IntegerField()

    class Meta():
        db_table = 'order_products'

# class DeliveryInfo(models.Model):
#     order_product   = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
#     company         = models.CharField(max_length=45)
#     tracking_number = models.CharField(max_length=45)

#     class Meta():
#         db_table = 'delivery_infos'

# Wish List
class WishProduct(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta():
        db_table = 'wish_products'

# recently viewed
class ViewedProduct(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta():
        db_table = 'viewed_products'