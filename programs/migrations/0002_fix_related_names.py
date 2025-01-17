# Generated by Django 3.0.6 on 2020-05-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_program_section_activity_option_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='options',
            field=models.ManyToManyField(related_name='activities', to='programs.Option'),
        ),
        migrations.AlterField(
            model_name='program',
            name='sections',
            field=models.ManyToManyField(related_name='programs', to='programs.Section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='activities',
            field=models.ManyToManyField(related_name='sections', to='programs.Activity'),
        ),
    ]
