from django.db import models
from django.utils import timezone

class CA(models.Model):

    organization = models.CharField(max_length=200)
    organization_unit = models.CharField(max_length=200)
    country = models.CharField(max_length=2)
    state = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200)
    algorithm = models.CharField(max_length=200)
    CRL_name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    valid_period = models.CharField(max_length=200)
    private_key = models.CharField(max_length=1000 )
    public_key = models.CharField(max_length=1000)

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.common_name

class Issuer(models.Model):

    organization = models.CharField(max_length=200)
    country = models.CharField(max_length=2)
    state = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    valid_period = models.CharField(max_length=200)
    private_key = models.CharField(max_length=1000 )
    public_key = models.CharField(max_length=1000)

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.common_name
