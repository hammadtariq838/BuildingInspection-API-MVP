# Generated by Django 5.0.4 on 2024-05-15 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_asset_file_childasset_projecttemplate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetresult',
            name='metadata',
            field=models.JSONField(blank=True, null=True),
        ),
    ]