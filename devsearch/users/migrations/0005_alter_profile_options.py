# Generated by Django 4.2.2 on 2023-06-29 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created_at']},
        ),
    ]
