from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name="شماره تماس")
    city = models.CharField(max_length=100, blank=True, verbose_name="شهر")
    address = models.TextField(blank=True, verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="کد پستی")

    def __str__(self):
        return self.username
