# Generated by Django 5.1.3 on 2024-12-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppl', '0008_alter_exercice_r_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='answer_type',
            field=models.CharField(choices=[('T', 'Text'), ('L', 'List'), ('I', 'Integer')], default='T', max_length=1),
        ),
    ]
