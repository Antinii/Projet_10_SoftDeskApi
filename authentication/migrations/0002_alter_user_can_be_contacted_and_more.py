# Generated by Django 5.0.3 on 2024-03-19 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='can_be_contacted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='can_data_be_shared',
            field=models.BooleanField(default=False),
        ),
    ]