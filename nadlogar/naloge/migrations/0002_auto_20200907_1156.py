# Generated by Django 3.1.1 on 2020-09-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naloge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='naloga',
            name='podatki',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='naloga',
            name='generator',
            field=models.CharField(choices=[('NalogaIzlociVsiljivcaSpol', 'Izloči vsiljivca - spol'), ('NajdiVsiljivcaBesednaVrsta', 'Izloči vsiljivca - besedna vrsta'), ('NajdiVsiljivcaStevilo', 'Izloči vsiljivca - slovnično število'), ('NajdiVsiljivcaPredmetnoPodrocje', 'Izloči vsiljivca - predmetno področje'), ('NalogaVstaviUstreznoObliko', 'Vstavi ustrezno obliko besede'), ('NalogaDolociSlovnicnoStevilo', 'Določevanje slovničnega števila'), ('NalogaDolociSteviloPomenov', 'Določi število pomenov - Franček'), ('NalogaGlasVsiljivec', 'Izloči vsiljivca - glas')], max_length=60),
        ),
    ]