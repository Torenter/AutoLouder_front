# Generated by Django 3.0.4 on 2021-02-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
