# Generated by Django 2.2.1 on 2019-07-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_monitor', '0002_auto_20190719_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='room_allocation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_monitor.RoomAllocation'),
        ),
    ]
