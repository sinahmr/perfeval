# Generated by Django 2.0.5 on 2018-06-19 12:48

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='admin',
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='employee',
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='نام خانوادگی'),
        ),
    ]
