# Generated by Django 3.0.3 on 2020-04-30 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListOfCountries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Country', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Infected', models.IntegerField()),
                ('Recoverd', models.IntegerField()),
                ('Dead', models.IntegerField()),
                ('Country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.ListOfCountries')),
            ],
        ),
    ]
