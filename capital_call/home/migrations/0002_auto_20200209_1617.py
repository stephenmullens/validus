# Generated by Django 3.0.3 on 2020-02-09 16:17

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingCalls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tag', models.CharField(blank=True, max_length=256, null=True)),
                ('date', models.DateField()),
                ('investment_name', models.CharField(max_length=256)),
                ('capital_required', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='commitments',
            name='amount_assigned',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
        migrations.AddField(
            model_name='commitments',
            name='is_exhausted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='FundingCallsComposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('commitment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundingcallscomposition_commitments', to='home.Commitments')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundingcallscomposition_funds', to='home.Funds')),
                ('funding_call', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundingcallscomposition_fundingcalls', to='home.FundingCalls')),
            ],
        ),
    ]
