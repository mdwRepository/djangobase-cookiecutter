# Generated by Django 3.2.13 on 2022-06-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
