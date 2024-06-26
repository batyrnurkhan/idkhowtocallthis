# Generated by Django 5.0.2 on 2024-05-10 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0004_alter_careeranchorquestion_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MapQuestion",
        ),
        migrations.DeleteModel(
            name="MapQuestion_kk",
        ),
        migrations.AlterModelOptions(
            name="careeranchorquestion",
            options={
                "verbose_name": '4. Тест "Якоря карьеры" | Вопрос',
                "verbose_name_plural": '4. Тест "Якоря карьеры" | Вопросы',
            },
        ),
        migrations.AlterModelOptions(
            name="careeranchorquestion_kk",
            options={
                "verbose_name": '4. "Мансап зәкірі"тесті | сұрағы',
                "verbose_name_plural": '4. "Мансап зәкірі"тесті | сұрақтары',
            },
        ),
        migrations.AlterModelOptions(
            name="careeranchorresponse",
            options={
                "verbose_name": '4. Тест "Якоря карьеры" | Вопрос и ответ',
                "verbose_name_plural": '4. Тест "Якоря карьеры" | Вопросы и ответы',
            },
        ),
        migrations.AlterModelOptions(
            name="hollandquestion",
            options={
                "verbose_name": "2. Тест-опросник на определение типа личности | Вопрос и ответы",
                "verbose_name_plural": "2. Тест-опросник на определение типа личности |Вопросы ответы второго теста",
            },
        ),
        migrations.AlterModelOptions(
            name="hollandquestion_kk",
            options={
                "verbose_name": "2. Тұлға түрін анықтауға арналған тест-сауалнама | сұрағы және жауабы",
                "verbose_name_plural": "2. Тұлға түрін анықтауға арналған тест-сауалнама | сұрақтары және жауабтары",
            },
        ),
        migrations.AlterModelOptions(
            name="preferencequestion",
            options={
                "verbose_name": "3. Тест на профессиональные предпочтения | Вопрос и ответ",
                "verbose_name_plural": "3. Тест на профессиональные предпочтения | Вопросы и ответы",
            },
        ),
        migrations.AlterModelOptions(
            name="preferencequestion_kk",
            options={
                "verbose_name": "3. Кәсіби артықшылық сынағы | сұрағы және жауабтары",
                "verbose_name_plural": "3. Кәсіби артықшылық сынағы | сұрақтары және жауабтары",
            },
        ),
        migrations.AlterModelOptions(
            name="question",
            options={
                "verbose_name": "1. Тест-опросник на профориентацию | Вопрос и ответы",
                "verbose_name_plural": "1. Тест-опросник на профориентацию | Вопросы и ответы",
            },
        ),
        migrations.AlterModelOptions(
            name="question_kk",
            options={
                "verbose_name": "1. Тест-опросник на профориентацию | сұрақтар және жауабтар",
                "verbose_name_plural": "1. Тест-опросник на профориентацию | сұрақтары және жауабтары",
            },
        ),
    ]
