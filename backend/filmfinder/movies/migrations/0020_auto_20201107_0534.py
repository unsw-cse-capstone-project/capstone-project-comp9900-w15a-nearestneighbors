# Generated by Django 3.1.2 on 2020-11-07 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_auto_20201107_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie_genre',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre', to='movies.movie'),
        ),
    ]
