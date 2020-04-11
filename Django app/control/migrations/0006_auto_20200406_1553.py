# Generated by Django 3.0.5 on 2020-04-06 19:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_auto_20200406_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='locks',
            name='button',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='No Name', max_length=70)),
                ('number', models.IntegerField(default=1)),
                ('floor', models.IntegerField(default=1)),
                ('lab', models.BooleanField(default=0)),
                ('capacity', models.IntegerField(default=30)),
                ('status', models.BooleanField(default=1)),
                ('createAt', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updatedBy', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('lock', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='control.Locks', verbose_name='Locks')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Rooms', verbose_name='Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Building', verbose_name='Building')),
            ],
        ),
    ]