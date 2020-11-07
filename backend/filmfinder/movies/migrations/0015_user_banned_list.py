# Generated by Django 3.1.2 on 2020-11-05 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20201103_0324'),
        ('movies', '0014_auto_20201103_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_banned_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banned_user_set', to='login.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_set', to='login.user')),
            ],
            options={
                'unique_together': {('user', 'banned_user')},
            },
        ),
    ]