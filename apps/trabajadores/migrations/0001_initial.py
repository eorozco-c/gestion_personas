# Generated by Django 2.2.4 on 2021-09-07 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresas', '0001_initial'),
        ('beneficios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sector_empresa', to='empresas.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('rut', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrabajadorBeneficio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elemento', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beneficio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trabajador_beneficio', to='beneficios.Beneficio')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficio_trabajador', to='trabajadores.Trabajador')),
            ],
        ),
        migrations.AddField(
            model_name='trabajador',
            name='beneficio',
            field=models.ManyToManyField(through='trabajadores.TrabajadorBeneficio', to='beneficios.Beneficio'),
        ),
        migrations.AddField(
            model_name='trabajador',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trabajador_empresa', to='empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='trabajador',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trabajador_sector', to='trabajadores.Sector'),
        ),
    ]
