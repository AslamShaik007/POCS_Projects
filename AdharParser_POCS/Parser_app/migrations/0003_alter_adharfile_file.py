# Generated by Django 4.2.6 on 2023-11-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parser_app', '0002_adharfile_address_adharfile_adhar_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adharfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
