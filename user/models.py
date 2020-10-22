# autopep8: off
from django.db import models


class User(models.Model):
    account         = models.CharField(max_length=45)
    password        = models.CharField(max_length=600)
    name            = models.CharField(max_length=45)
    email           = models.EmailField(max_length=254)
    phone_number    = models.CharField(max_length=45)
    date_of_birth   = models.DateField(auto_now=False, auto_now_add=False, null=True)
    sms_agreement   = models.BooleanField()
    email_agreement = models.BooleanField()

    class Meta:
        db_table = "users"


class Address(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    address          = models.CharField(max_length=200)
    detailed_address = models.CharField(max_length=200)
    zip_code         = models.IntegerField()

    class Meta:
        db_table = "addresses"
