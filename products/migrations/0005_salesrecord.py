# Generated by Django 3.2.3 on 2021-06-20 18:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20210612_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('product_sold', models.CharField(max_length=30)),
                ('liters_sold', models.FloatField()),
                ('price', models.FloatField()),
                ('measure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='products.measure')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
