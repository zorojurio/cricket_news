# Generated by Django 2.2.8 on 2019-12-27 17:15

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='long_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
