# Generated by Django 5.0.1 on 2024-01-25 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0001_initial'),
        ('user_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdditional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='static/images/avatars/default.jpg', upload_to='static/images/avatars/', verbose_name='avatar')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='birthday')),
                ('favorite_posts', models.ManyToManyField(related_name='favorite_posts', to='post_app.post')),
                ('linked_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='linked_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='BlogUser',
        ),
    ]
