# Generated by Django 4.0 on 2022-01-03 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tl2175app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='stationProvider',
            field=models.ForeignKey(db_column='providerName', on_delete=django.db.models.deletion.CASCADE, to='tl2175app.provider'),
        ),
    ]
