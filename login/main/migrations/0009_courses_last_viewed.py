# Generated by Django 4.2 on 2023-05-12 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_profile_courses_publishrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='last_viewed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
