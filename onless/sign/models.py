from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    start = models.CharField(max_length=5, blank=True)
    stop = models.CharField(max_length=5, blank=True)
    text = models.TextField(max_length=5000)
    photo = models.ImageField(upload_to='sign/')

    def __str__(self):
        return self.title


class Sign(models.Model):
    code = models.CharField(max_length=5)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=5000)

    def __str__(self):
        return self.title
