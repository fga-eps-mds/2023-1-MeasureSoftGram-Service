# Generated by Django 4.0.6 on 2022-07-16 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_collectedmetric_supportedmetric_delete_measure_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectedmetric',
            options={'ordering': ['created_at']},
        ),
    ]
