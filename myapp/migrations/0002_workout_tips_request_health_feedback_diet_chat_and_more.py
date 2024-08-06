# Generated by Django 4.2.5 on 2024-08-06 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=3000)),
                ('video', models.CharField(max_length=500)),
                ('TRAINER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.trainer')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='tips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=3000)),
                ('TRAINER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.trainer')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=200)),
                ('BATCH', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.batch')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='health',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.CharField(max_length=3)),
                ('weight', models.CharField(max_length=3)),
                ('activelevel', models.CharField(max_length=30)),
                ('medical', models.CharField(max_length=500)),
                ('bmi', models.CharField(max_length=10)),
                ('foodtype', models.CharField(max_length=10)),
                ('target', models.CharField(max_length=10)),
                ('targetweight', models.CharField(default='', max_length=10)),
                ('estimatedtime', models.CharField(default='', max_length=10)),
                ('weeklytarget', models.CharField(default='', max_length=10)),
                ('allergies', models.CharField(default='None', max_length=500)),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20)),
                ('feedback', models.CharField(max_length=2000)),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('title', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=3000)),
                ('TRAINER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.trainer')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('usertype', models.CharField(max_length=10)),
                ('chat', models.CharField(max_length=300)),
                ('TRAINER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.trainer')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20)),
                ('REQUEST', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.request')),
                ('TRAINER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.trainer')),
            ],
        ),
    ]
