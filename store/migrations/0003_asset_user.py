# Generated by Django 3.2.4 on 2021-06-28 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('store', '0002_alter_commentrating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
            preserve_default=False,
        ),
    ]
