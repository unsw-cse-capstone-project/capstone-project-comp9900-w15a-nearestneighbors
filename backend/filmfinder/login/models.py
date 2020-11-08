from django.db import models


# Create your models here.
# a custom CharField that treats all letters as lower case
class lower_CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(lower_CharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='../movies/user_dp', blank=True)
    email = models.CharField(max_length=50, default='N/A')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['uid']
        verbose_name = 'user'


