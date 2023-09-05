# Generated by Django 3.2.15 on 2022-11-03 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Managers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('managername', models.CharField(default='', max_length=100)),
                ('teamname', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Highlight', max_length=50)),
                ('priority', models.IntegerField(default=4)),
                ('service', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('entry_owner', models.CharField(max_length=300)),
                ('entry', models.TextField(default='')),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('team', models.CharField(default='', max_length=100)),
                ('unit', models.CharField(default='', max_length=100)),
                ('manager', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicename', models.CharField(default='', max_length=100)),
                ('username', models.CharField(default='', max_length=100)),
                ('teamname', models.CharField(default='', max_length=100)),
                ('unitname', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamname', models.CharField(default='', max_length=100)),
                ('unitname', models.CharField(default='', max_length=100)),
                ('manager_mail', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitname', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('teamname', models.CharField(default='', max_length=100)),
                ('unitname', models.CharField(default='', max_length=100)),
                ('mail', models.CharField(default='', max_length=200)),
                ('phone', models.CharField(default='', max_length=15)),
            ],
        ),
    ]