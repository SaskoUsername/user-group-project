from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'groups'


class User(AbstractUser):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'користувач'
        verbose_name_plural = 'користувачі'
