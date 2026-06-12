from django.db import models


class FakeModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    national_code = models.CharField(max_length=10)
