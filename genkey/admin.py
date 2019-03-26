from django.contrib import admin
from .models import CA, Issuer
# Register your models here.
admin.site.register(CA)
admin.site.register(Issuer)