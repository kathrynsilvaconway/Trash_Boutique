import bcrypt
from django.db import models
import re

from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
class UserManager(models.Manager):
    def reg_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_regex.match(postData['email']):
            errors['email'] = "Pleas enter a valid email address."
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['emailAlreadyExists'] ="There is already an account associated with this email address."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if postData['first_name'].isalpha() == False:
            errors['first_name'] = "Frist name must contain only letters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last name must contain only letters."
        if len(postData['password']) < 5:
            errors['password_length'] = "Password must be at least 5 characters."
        if postData['password'] != postData['conf_password']:
            errors['password_no_match'] = 'Passwords do not match'
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if len(user) == 0:
            errors['bad_email'] = "We can't find an account for that email address."

        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) == False:
            errors['bad_password'] = "Password is incorrect."
        return errors
    
    def update_validator(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_regex.match(postData['email']):
            errors['email'] = "Pleas enter a valid email address."
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name is required."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "last name is required."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )
    objects = UserManager()

class Cat(models.Model):
    cat_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    price = models.FloatField()
    cat = models.ForeignKey(Cat, related_name='items', on_delete=CASCADE)
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def avg_stars(self):
        total = 0
        list = []
        for x in self.item_reviews.all():
            total += x.stars
            list.append(x.stars)
            avg = total / len(list)
        return round(avg, 1)
        

class Review(models.Model):
    review = models.TextField()
    title = models.TextField()
    user = models.ForeignKey(User, related_name='my_reviews', on_delete=CASCADE)
    item = models.ForeignKey(Item, related_name='item_reviews', on_delete=CASCADE)
    stars = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='item_orders')
    total = models.FloatField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Item, related_name='cart_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)