# Generated by Django 2.0.5 on 2018-07-12 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0004_auto_20180705_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='scales',
        ),
        migrations.RemoveField(
            model_name='season',
            name='endDate',
        ),
    ]