# Generated by Django 3.0.5 on 2020-04-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20200423_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelanguage',
            name='tutor',
            field=models.BooleanField(default=False, verbose_name='co-host'),
        ),
    ]