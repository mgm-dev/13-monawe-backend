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

class Group(models.Model):
    name       = models.CharField(max_length=45)
    category   = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'groups'

class Product(models.Model):
    name       = models.CharField(max_length=45)
    group      = models.ForeignKey(Group, on_delete=models.CASCADE)
    price      = models.IntegerField()
    origin     = models.CharField(max_length=45)
    company    = models.CharField(max_length=45)
    stock      = models.IntegerField(null=True)
    date       = models.DateField(auto_now=False)
    attribute  = models.TextField(null=True)
    gift       = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'products'


# product detail/option

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    stock = models.IntegerField()
    plus_price = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_options'

class ProdcutImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_images'


class Attribute(models.Model):
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'attributes'

class ProductAttribute(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_attributes'

class Color(models.Model):
    color = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colors'

class Thickness(models.Model):
    thickness = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'thicknesses'

class BodyColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'body_colors'

class InkColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ink_colors'

class ProductThickness(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Thickness, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_thickness'

