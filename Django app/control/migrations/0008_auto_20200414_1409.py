# Generated by Django 3.0.5 on 2020-04-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_control_entrada'),
    ]

    operations = [
        migrations.RenameField(
            model_name='control',
            old_name='entrada',
            new_name='horaEntrada',
        ),
        migrations.AddField(
            model_name='control',
            name='accion',
            field=models.CharField(default='', max_length=70),
        ),
    ]