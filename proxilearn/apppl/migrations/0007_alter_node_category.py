# Generated by Django 5.1.3 on 2024-11-29 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppl', '0006_alter_node_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='category',
            field=models.CharField(choices=[('M', 'Typem'), ('MM', 'Typemm'), ('R', 'Typer'), ('RM', 'Typerm')], default='M', max_length=2),
        ),
    ]
