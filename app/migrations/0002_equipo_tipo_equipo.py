# Generated by Django 4.2 on 2024-10-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id_equipo', models.AutoField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('serie', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('id_cliente', models.IntegerField()),
                ('id_tipo_equipo', models.IntegerField()),
            ],
            options={
                'db_table': 'equipo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo_equipo',
            fields=[
                ('id_tipo_equipo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('activo', models.BooleanField()),
            ],
            options={
                'db_table': 'tipo_equipo',
                'managed': True,
            },
        ),
    ]
