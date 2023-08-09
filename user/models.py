from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    password = models.CharField(max_length=20) #criar form dps
    authority = models.BooleanField()

    # class Meta:
    #     app_label = 'user'