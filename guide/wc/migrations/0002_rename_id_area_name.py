# Generated by Django 3.2.3 on 2021-06-10 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wc', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='id',
            new_name='name',
        ),
    ]