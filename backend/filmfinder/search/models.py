from django.db import models

# Create your models here.
# a custom CharField that treats all letters as lower case
class lower_CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(lower_CharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()