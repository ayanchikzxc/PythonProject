# Generated by Django 5.1.7 on 2025-04-11 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryApp', '0002_entry_remove_diaryentry_tags_remove_diaryentry_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='DiaryEntry',
        ),
    ]
