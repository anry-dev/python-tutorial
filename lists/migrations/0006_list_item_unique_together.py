# Generated by Django 3.2.15 on 2023-01-31 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_alter_item_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]