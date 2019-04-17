from django.db import models
from django.utils import timezone
from accounts.models import User
# Create your models here.


class CSR(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    organization_unit = models.CharField(max_length=200)
    country = models.CharField(max_length=2)
    state = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200)
    algorithm = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    private_key = models.CharField(max_length=10000)
    public_key = models.CharField(max_length=1000)
    pem = models.CharField(max_length=10000)
    created_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.common_name