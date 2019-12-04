# Generated by Django 2.0 on 2019-12-04 17:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_auto_20191202_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Cinemas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'CinemaComments',
            },
        ),
        migrations.AlterField(
            model_name='orders',
            name='timestamp',
            field=models.TimeField(default=datetime.date(2019, 12, 4)),
        ),
    ]