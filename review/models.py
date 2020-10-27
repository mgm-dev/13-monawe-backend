# autopep8: off
from django.db      import models
from product.models import Product
from user.models    import User

class ProductReview(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating     = models.DecimalField(max_digits=2, decimal_places=1)
    title      = models.CharField(max_length=45)
    content    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url  = models.URLField(max_length=200, null=True)

    class Meta():
        db_table  = 'product_reviews'
