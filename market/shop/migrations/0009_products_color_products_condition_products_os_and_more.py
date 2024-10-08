# Generated by Django 5.0.6 on 2024-08-21 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(default='Input Color', max_length=20),
        ),
        migrations.AddField(
            model_name='products',
            name='condition',
            field=models.CharField(default='Input Product Condition', max_length=20),
        ),
        migrations.AddField(
            model_name='products',
            name='os',
            field=models.CharField(default='Operating System Type', max_length=20),
        ),
        migrations.AddField(
            model_name='products',
            name='storage',
            field=models.CharField(default='Input Storage Cap', max_length=20),
        ),
    ]
