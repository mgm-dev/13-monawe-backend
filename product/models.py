# autopep8: off
from django.db   import models
from user.models import User

# product heirarchy
class Field(models.Model):
    name    = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'fields'

class Category(models.Model):
    name    = models.CharField(max_length=45)
    field   = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'categories'

class Subcategory(models.Model):
    name       = models.CharField(max_length=45)
    category   = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'subcategories'

class Product(models.Model):
    name         = models.CharField(max_length=45)
    subcategory  = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    origin       = models.CharField(max_length=45)
    company      = models.CharField(max_length=45)
    created_at   = models.DateField(auto_now=False)
    updated_at   = models.DateField(auto_now=False)
    description  = models.TextField(null=True)
    sales_amount = models.IntegerField(null=True)
    thumb_nail   = models.URLField(max_length=200, null=True)

    def get_info(self):
        data = {
            'id'              : self.id,
            'name'            : self.name,
            'price'           : int(self.price),
            'subcategory_id'  : self.subcategory.id,
            'subcategory_name': Subcategory.objects.get(id=self.subcategory_id).name,
            'created_at'      : self.created_at,
            'company'         : self.company,
            'description'     : self.description,
            'sales_amount'    : self.sales_amount,
            'image_url'       : self.thumb_nail
        }

        return data

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'products'

class ProductImage(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url   = models.CharField(max_length=500)

    class Meta():
        db_table = 'product_images'

# product colors

class Color(models.Model):
    name     = models.CharField(max_length=45)
    hex_code = models.CharField(max_length=45, default='000000')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colors'

# product thickness

class Thickness(models.Model):
    value = models.CharField(max_length=45)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'thicknesses'

# product detail/option

class ProductOption(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    body_color  = models.ForeignKey(Color, related_name ="body_color", on_delete=models.CASCADE, null=True)
    ink_color   = models.ForeignKey(Color, related_name ="ink_color", on_delete=models.CASCADE, null=True)
    thickness   = models.ForeignKey(Thickness,on_delete=models.CASCADE, null=True)
    stock       = models.IntegerField(null=True)
    plus_price  = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    etc_option  = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'product_options'

# product tags

class Tag(models.Model):
    name = models.CharField(max_length=45)
    product = models.ManyToManyField(Product, through='ProductTag')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'

class ProductTag(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag       = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_tags'
