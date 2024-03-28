# Generated by Django 4.0.6 on 2024-03-28 14:17

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
            name='Category',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('color', models.CharField(blank=True, default='#525252', max_length=7, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField()),
                ('price', models.FloatField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(to='items_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(default='items_app/ItemImage/default.png', upload_to='items_app/ItemImage')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items_app.item')),
            ],
        ),
    ]