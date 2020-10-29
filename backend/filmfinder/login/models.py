from django.db import models


# Create your models here.
class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    profile_photo = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['uid']
        verbose_name = 'user'


