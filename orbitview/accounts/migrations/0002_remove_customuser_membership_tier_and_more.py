# Generated by Django 5.1.2 on 2024-10-17 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='membership_tier',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='subscription_expiry',
        ),
    ]
