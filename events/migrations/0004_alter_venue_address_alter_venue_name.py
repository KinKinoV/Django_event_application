# Generated by Django 4.0.5 on 2023-01-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_venue_address_alter_venue_email_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(max_length=300, verbose_name='Vanue address'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=120, verbose_name='Vanue Name'),
        ),
    ]
