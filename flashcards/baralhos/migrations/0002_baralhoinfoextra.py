# Generated by Django 4.1.5 on 2023-01-16 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baralhos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaralhoInfoExtra',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('baralhos.baralho',),
        ),
    ]
