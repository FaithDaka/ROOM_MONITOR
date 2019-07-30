# Generated by Django 2.2.1 on 2019-07-17 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayOfTheWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbr', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], max_length=3)),
                ('group_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('size', models.FloatField()),
                ('power_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoomAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_monitor.Group')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_monitor.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('start_time', models.IntegerField()),
                ('end_time', models.IntegerField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_monitor.DayOfTheWeek')),
                ('room_allocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_monitor.RoomAllocation')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_monitor.Programme'),
        ),
    ]