# Generated by Django 3.0.7 on 2020-06-05 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permafrost', '0012_remove_permafrostrole_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='permafrostrole',
            name='category',
            field=models.CharField(blank=True, choices=[('administrator', 'Administrator'), ('staff', 'Staff'), ('user', 'User')], max_length=32, null=True, verbose_name='Category'),
        ),
    ]
