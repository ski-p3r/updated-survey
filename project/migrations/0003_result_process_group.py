# Generated by Django 5.0.2 on 2024-02-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_question_process_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='process_group',
            field=models.CharField(blank=True, choices=[('initiating', 'Initiating'), ('planning', 'Planning'), ('executing', 'Executing'), ('m&c', 'M & C'), ('closing', 'Closing')], max_length=20, null=True),
        ),
    ]
