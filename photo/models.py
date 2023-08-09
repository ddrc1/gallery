from django.db import models
from user.models import User


class Photo(models.Model):
    image = models.ImageField(upload_to='uploads')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)