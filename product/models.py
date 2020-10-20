from django.db import models

# autopep8: off


# product heirarchy
class Fields(models.Model):
    name    = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'fields'

class Categories(models.Model):
    name    = models.CharField(max_length=45)
    field   = models.ForeignKey(Fields, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'categories'

class Groups(models.Model):
    name       = models.CharField(max_length=45)
    category   = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'groups'

class Products(models.Model):
    name       = models.CharField(max_length=45)
    group      = models.ForeignKey(Groups, on_delete=models.CASCADE)
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


# product detail/optiondjango

class ProductOptions(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    stock = models.IntegerField()
    plus_price = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_options'

class ProdcutImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_images'


class Attributes(models.Model):
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'attributes'

class ProductAttributes(models.Model):
    product   = models.ForeignKey(Products, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_attributes'

class Colors(models.Model):
    color = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colors'

class Thicknesses(models.Model):
    thickness = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'thicknesses'

class BodyColors(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    color   = models.ForeignKey(Colors, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'body_colors'

class InkColors(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    color   = models.ForeignKey(Colors, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ink_colors'

class ProductThicknesses(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    color   = models.ForeignKey(Thicknesses, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_thickness'

