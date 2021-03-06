# Generated by Django 3.0.5 on 2020-04-22 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='country')),
                ('timezone', timezone_field.fields.TimeZoneField(blank=True, null=True, verbose_name='timezone')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_set', to=settings.AUTH_USER_MODEL, verbose_name='reported by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutor', models.BooleanField(default=False, verbose_name='tutor')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.Language', verbose_name='language')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='profile')),
            ],
            options={
                'unique_together': {('profile', 'language')},
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(blank=True, through='profiles.ProfileLanguage', to='languages.Language', verbose_name='language'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
