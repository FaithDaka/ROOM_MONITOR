# Generated by Django 2.2.1 on 2019-07-19 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_monitor', '0004_auto_20190719_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='room_allocation',
        ),
        migrations.AddField(
            model_name='lecture',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='room_monitor.Group'),
            preserve_default=False,
        ),
    ]
