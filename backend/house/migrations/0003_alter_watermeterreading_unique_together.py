# Generated by Django 5.0.7 on 2024-07-17 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0002_alter_apartment_number_alter_house_house_number_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watermeterreading',
            unique_together=set(),
        ),
    ]
