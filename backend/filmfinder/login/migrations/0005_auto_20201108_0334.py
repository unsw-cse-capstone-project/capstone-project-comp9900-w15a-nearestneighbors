# Generated by Django 3.1.2 on 2020-11-08 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20201103_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='../movies/user_dp'),
        ),
    ]
