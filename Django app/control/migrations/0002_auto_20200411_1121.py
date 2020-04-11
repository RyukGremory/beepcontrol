# Generated by Django 3.0.5 on 2020-04-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='subject',
            name='credits',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='prerequirements',
            field=models.CharField(default='', max_length=70),
        ),
    ]