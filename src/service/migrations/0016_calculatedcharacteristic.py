# Generated by Django 4.0.6 on 2022-08-08 15:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0015_merge_20220807_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatedCharacteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('characteristic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calculated_characteristics', to='service.supportedcharacteristic')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
