# Generated by Django 2.0 on 2018-03-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0006_post_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='abstract',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]