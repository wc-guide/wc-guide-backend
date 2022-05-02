# Generated by Django 3.2.3 on 2021-09-06 08:36

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wc', '0002_rename_id_area_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherArea',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('properties', models.JSONField(blank=True, default=None, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, default=None, null=True, srid=4326)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='others', to='wc.otherarea')),
            ],
        ),
    ]