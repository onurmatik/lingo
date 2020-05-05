# Generated by Django 3.0.5 on 2020-05-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20200503_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='level',
            field=models.CharField(blank=True, choices=[('A', 'I can catch some words in texts or speeches. From time to time, by combining these words, I can grasp the context and the general meaning, but I cannot get a complete idea of the content of the text / speech; I have a hard time speaking / I cannot speak.'), ('B', 'When I read simple texts, I can get a rough idea of the general subject; I can understand the main idea of slow and clear conversations; I cannot understand complex texts or speeches; I have difficulty speaking / I cannot speak.'), ('C', 'I can understand texts / speeches mostly unless they are complex, but I want to grasp more and master the whole. I can speak slowly with a limited vocabulary, I want to be fluent, improve my vocabulary.')], max_length=1, null=True, verbose_name='level'),
        ),
    ]
