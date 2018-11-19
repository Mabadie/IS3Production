# Generated by Django 2.1.2 on 2018-11-19 04:00

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
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('author', models.TextField()),
                ('year', models.IntegerField(default=False)),
                ('image', models.CharField(blank=True, max_length=100)),
                ('aviable', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
