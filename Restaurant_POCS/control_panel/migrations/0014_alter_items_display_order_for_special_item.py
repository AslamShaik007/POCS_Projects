# Generated by Django 5.0.3 on 2024-03-19 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0013_alter_adminprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='display_order_for_special_item',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
