# Generated by Django 5.0.3 on 2024-05-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0019_alter_addtocartitems_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
