# Generated by Django 3.0.5 on 2020-04-29 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20200426_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
