# Generated by Django 2.2 on 2021-11-13 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0010_auto_20211023_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='stars',
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='this_item_stars', to='ecomm_app.User')),
            ],
        ),
    ]
