# Generated by Django 5.2 on 2025-04-28 09:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('dueDate', models.DateTimeField()),
                ('status', models.CharField(choices=[('notStarted', 'NotStarted'), ('pending', 'Pending'), ('done', 'Done')], default='notStarted', max_length=20)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='farms.farm')),
            ],
        ),
    ]
