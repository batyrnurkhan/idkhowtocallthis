# Generated by Django 5.0.2 on 2024-02-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_remove_choice_question_delete_result_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HollandQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='Из каждой пары профессий нужно указать одну, предпочитаемую', max_length=1024)),
                ('choice_a', models.CharField(max_length=512)),
                ('choice_b', models.CharField(max_length=512)),
            ],
        ),
    ]
