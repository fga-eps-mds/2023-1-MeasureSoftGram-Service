# Generated by Django 4.0.6 on 2022-07-26 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_supportedmetric_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calculatedmeasure',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='collectedmetric',
            options={'ordering': ['-created_at']},
        ),
    ]
