# Generated by Django 3.1.6 on 2021-03-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0007_auto_20210311_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfile',
            name='log',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='LogFile'),
        ),
    ]
