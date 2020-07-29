from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Role(models.Model):
    role_name = models.CharField(max_length = 20)

class Hero(models.Model):
    hero_name = models.CharField(max_length = 50)
    attribute = models.CharField(max_length = 12)
    attack_type = models.CharField(max_length = 6)
    roles = models.ManyToManyField(Role)

class Guide(models.Model):
    guide_name = models.CharField(max_length = 30)
    guide_body = models.TextField(max_length = 2000)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='guides', null= True)
    hero = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(119), MinValueValidator(1)]
     )
    published = models.BooleanField(null=True)

class Item(models.Model):
    item_name= models.CharField(max_length = 50)
    item_description = models.CharField(max_length = 250)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='items')

