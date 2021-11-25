# Generated by Django 3.2.9 on 2021-11-25 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoxofficeMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('rank', models.IntegerField()),
                ('rank_inten', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('genre_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_code', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('release_date', models.DateField(null=True)),
                ('director', models.CharField(max_length=30, null=True)),
                ('plot', models.TextField(default='')),
                ('showtime', models.IntegerField(null=True)),
                ('poster_path', models.TextField(default='', null=True)),
                ('vote_average', models.FloatField(null=True)),
                ('genre', models.ManyToManyField(related_name='movie_genre', to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('character_number', models.IntegerField()),
                ('eng_name', models.CharField(max_length=20)),
                ('genre', models.ManyToManyField(related_name='character_genre', to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('movie_code', models.ManyToManyField(related_name='movie_actor', to='movies.Movie')),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
    ]
