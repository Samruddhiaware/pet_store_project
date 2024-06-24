# Generated by Django 5.0.6 on 2024-06-04 06:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_customer1_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('totalamount', models.FloatField()),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.customer1')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.pet')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]