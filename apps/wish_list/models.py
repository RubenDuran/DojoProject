from __future__ import unicode_literals
from django.db import models
import bcrypt


class UserManager(models.Manager):

    def validate(self, post):
        errors = []
        if len(post['name']) < 3:
            errors.append('Name must be at least 3 characters long')
        if not post['name'].isalpha():
            errors.append('Name can only contain letters')
        if len(post['username']) < 3:
            errors.append('Username must be at least 3 characters long')
        if len(post['pw']) < 8:
            errors.append('password must be at least 8 characters long')
        if post['pw'] != post['pwconf']:
            errors.append('password and confirmation fields do not match')
        check_user = self.filter(username=post['username'])
        if check_user:
            errors.append('Username already exist in the database')
        return errors

    def signin(self, post):
        errors = []
        if len(post['username']) < 3:
            errors.append('username must be at least 3 characters long')
        elif len(post['pw']) < 8:
            errors.append('password must be at least 8 characters long')
        else:
            username = post['username']
            check_user = self.filter(username=post['username'])
            if not check_user:
                errors.append('no such user in database')
            else:
                pw_check = self.get(username=post['username'])
                pw = bcrypt.hashpw(post['pw'].encode(),
                                   pw_check.password.encode())
                if pw != pw_check.password:
                    errors.append('Incorect Password for user')
                else:
                    pass
        return errors


class ItemManager(models.Manager):

    def validate(self, post):
        errors = []
        if len(post['prod_name']) < 1:
            errors.append('Field may not be empty')
        if len(post['prod_name']) < 3:
            errors.append(
                'Product/Item name must be at least 3 characters long')
        check_product = self.filter(prod_name=post['prod_name'])
        if check_product:
            errors.append('Product already exist in the database')
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    date_hired = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


class Item(models.Model):
    prod_name = models.CharField(max_length=255)
    user = models.ForeignKey('User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ItemManager()


class Wishlist(models.Model):
    user = models.ForeignKey('User')
    item = models.ForeignKey('Item')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
