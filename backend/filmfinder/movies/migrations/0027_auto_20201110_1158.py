# Generated by Django 3.1.2 on 2020-11-10 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0026_moviefeatures'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviefeatures',
            old_name='mid',
            new_name='movie',
        ),
    ]
