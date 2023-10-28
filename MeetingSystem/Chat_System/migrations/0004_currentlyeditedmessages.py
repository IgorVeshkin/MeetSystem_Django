# Generated by Django 4.2.2 on 2023-10-19 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Chat_System', '0003_currentlydeletedmessages'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentlyEditedMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_message_id', models.IntegerField()),
                ('edited_message_text', models.TextField()),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Chat_System.chatroom')),
                ('message_editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
