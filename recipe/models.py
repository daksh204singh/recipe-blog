from django.db import models
from datetime import datetime

from django.forms import FileField
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=15)
    cat_icon = models.ImageField(upload_to='cat_images/', max_length=255 )
    cat_show =models.IntegerField()
    def __str__(self):
        return self.cat_name


class Recipe(models.Model):
    recipe_name=models.CharField(max_length=50)
    recipe_posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    recipe_img1= models.ImageField(upload_to='recipe_images/', max_length=255 )
    recipe_img2= models.ImageField(upload_to='recipe_images/', max_length=255)
    recipe_img3= models.ImageField(upload_to='recipe_images/', max_length=255)
    recipe_img4= models.ImageField(upload_to='recipe_images/', max_length=255)
    recipe_des =models.CharField(max_length=1000)
    recipe_ingredients =models.CharField(max_length=1000)
    recipe_servings =models.CharField(max_length=1000,null=True)
    recipe_sources =models.CharField(max_length=500,null=True)
    recipe_preptime =models.CharField(max_length=50)
    recipe_cooktime =models.CharField(max_length=50)
    recipe_cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    recipe_date=models.DateTimeField(default=datetime.now)
    votes = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    def update_rating(self, user_rating):
        self.rating *= self.votes
        self.votes += 1
        self.rating = round((self.rating + user_rating)/self.votes)
        self.save()
    def __str__(self):
        return self.recipe_name

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField(default=3)
    create_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.subject


def upload_to(param, param1):
    pass


class userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    profile_pic = models.ImageField(upload_to='recipe_profile_pic/',max_length=255)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)

