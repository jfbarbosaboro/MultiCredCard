# Generated by Django 3.0.6 on 2020-06-01 01:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CPF', models.CharField(max_length=11, unique=True)),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('DateOfBirth', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaxLimit', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('Client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MultiCredCardAPI.Client')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=16)),
                ('PrintedName', models.CharField(max_length=100)),
                ('ValidThruMonth', models.IntegerField()),
                ('ValidThruYear', models.IntegerField()),
                ('CVV', models.CharField(max_length=3)),
                ('Wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultiCredCardAPI.Wallet')),
            ],
        ),
    ]