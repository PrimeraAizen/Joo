# Generated by Django 4.2 on 2023-05-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
