from django.db import models

# Create your models here.


#product heirarchy
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
    stock      = models.IntegerField()
    date       = models.DateField(auto_now=False)
    attribute  = models.TextField(null=True)
    gift       = models.BooleanField()

    def __str__(self):
        return self.name
    
    class Meta():
        db_table = 'products'


#product detail/option
