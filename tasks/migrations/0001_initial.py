# Generated by Django 2.2.8 on 2020-02-07 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=200)),
                ('cat_description', models.TextField()),
                ('cat_order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['cat_order'],
            },
        ),
        migrations.CreateModel(
            name='Importance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imp_name', models.CharField(max_length=200)),
                ('imp_description', models.TextField()),
                ('imp_order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['imp_order'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sta_name', models.CharField(max_length=200)),
                ('sta_description', models.TextField()),
                ('sta_order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['sta_order'],
            },
        ),
    ]