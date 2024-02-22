# Generated by Django 5.0.2 on 2024-02-22 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.AddField(
            model_name='question',
            name='choice_a',
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='choice_b',
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=1024),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
    ]
