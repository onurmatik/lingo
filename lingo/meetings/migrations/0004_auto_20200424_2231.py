# Generated by Django 3.0.5 on 2020-04-24 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20200423_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='meeting password'),
        ),
        migrations.AlterField(
            model_name='meetingrequest',
            name='tutor',
            field=models.BooleanField(choices=[(False, 'participant'), (True, 'co-host')], default=False, verbose_name='co-host'),
        ),
    ]