from django.db import models

# autopep8: off


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
    price        = models.IntegerField()
    origin       = models.CharField(max_length=45)
    company      = models.CharField(max_length=45)
    create_at    = models.DateField(auto_now=False)
    updated_at   = models.DateField(auto_now=False, null=True, blank=True)
    description  = models.TextField(null=True)
    sales_amount = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'products'

class ProductImage(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url   = models.CharField(max_length=500)

    class Meta():
        db_table = 'product_images'


## product detail/option

# product colors

class Color(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colors'

class BodyColor(models.Model):  # middle table
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'body_colors'

class InkColor(models.Model):  # middle table
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ink_colors'

# product thickness

class Thickness(models.Model):
    value = models.CharField(max_length=45)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'thicknesses'


class ProductThicknesses(models.Model):  # middle table
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    thickness  = models.ForeignKey(Thickness, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_thicknesses'

# option

class ProductOption(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    body_color  = models.ForeignKey(BodyColor, on_delete=models.CASCADE, null=True)
    ink_color   = models.ForeignKey(InkColor, on_delete=models.CASCADE, null=True)
    thickness   = models.ForeignKey(Thickness, on_delete=models.CASCADE, null=True)
    stock       = models.IntegerField(null=True)
    plus_price  = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'product_options'

#product tags

class Tag(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'

class ProductTag(models.Model):  # middle table
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag       = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_tags'




