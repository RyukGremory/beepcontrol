# Generated by Django 3.0.5 on 2020-04-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0009_auto_20200414_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='accion',
            field=models.CharField(choices=[('A', 'Entrar'), ('C', 'Cerrar'), ('Z', 'Ciclo')], default='A', max_length=2),
        ),
    ]