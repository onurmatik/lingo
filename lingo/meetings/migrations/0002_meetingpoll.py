# Generated by Django 3.0.5 on 2020-04-23 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Poor'), (2, 'OK'), (3, 'Good')], verbose_name='rate')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting', verbose_name='meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
