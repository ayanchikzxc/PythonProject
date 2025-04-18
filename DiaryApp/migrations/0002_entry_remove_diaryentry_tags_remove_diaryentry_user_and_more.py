# Generated by Django 5.1.7 on 2025-04-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='diaryentry',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='diaryentry',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='diary_entry',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='DiaryEntry',
        ),
        migrations.DeleteModel(
            name='MediaFile',
        ),
    ]
