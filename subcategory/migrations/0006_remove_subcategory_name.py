# Generated by Django 3.0.5 on 2020-04-04 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subcategory', '0005_subcategory_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='name',
        ),
    ]