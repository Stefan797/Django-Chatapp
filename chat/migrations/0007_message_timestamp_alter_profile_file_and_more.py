# Generated by Django 4.0.2 on 2022-05-23 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_profile_status_alter_profile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.IntegerField(default=1653322601791),
        ),
        migrations.AlterField(
            model_name='profile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static/uploads'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
