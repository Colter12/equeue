# Generated by Django 5.0.7 on 2024-10-14 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0006_subcategory_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=models.TextField(default='Описание отсутствует'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='letter',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=1, unique=True),
        ),
    ]