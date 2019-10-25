# from django.db import models
# from django.utils import timezone
# import hashlib

# class UserData(models.Model):
#     slug = models.SlugField(max_length=255, unique=True,)
#     name = models.CharField(max_length=255, unique=True,)
#     password = models.CharField(max_length=255,)
#     bio = models.TextField(blank=True,)
#     favorite = models.ManyToManyField('Article', blank=True,)
#     create_date = models.DateField(default=timezone.now,)
#     icon = models.ImageField(blank=True, upload_to='icon')
#     del_flg = models.BooleanField(default=False,)


# class Article(models.Model):
#     slug = models.SlugField(max_length=255, unique=True,)
#     folder = models.ForeignKey('Folder', on_delete=models.CASCADE,)
#     author = models.ForeignKey('User', on_delete=models.CASCADE,)
#     private_flg = models.BooleanField(default=False,)
#     title = models.CharField(max_length=255,)
#     contents = models.TextField()
#     create_date = models.DateField(default=timezone.now,)
#     update_date = models.DateField(auto_now=True,)
#     del_flg = models.BooleanField(default=False,)
#     views = models.IntegerField(default=0,)


# class Comment(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     article = models.ForeignKey('Article', on_delete=models.CASCADE)
#     contents = models.TextField()
#     create_date = models.DateField(default=timezone.now,)
#     del_flg = models.BooleanField(default=False,)


# class Category(models.Model):
#     slug = models.SlugField(max_length=255, unique=True,)
#     author = models.ForeignKey('User', on_delete=models.CASCADE)
#     constant_flg = models.BooleanField(default=False,)
#     private_flg = models.BooleanField(default=False,)
#     title = models.CharField(max_length=255,)
#     create_date = models.DateField(default=timezone.now,)
#     del_flg = models.BooleanField(default=False,)


