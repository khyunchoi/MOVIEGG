import json
from .models import BoxofficeMovie
from django.shortcuts import render

# Create your views here.
def load(request):

    with open("./movies/movierank.json", "r", encoding='UTF8') as json_file:
        json_data = json.loads(json_file.read())

        for rec in json_data['boxOfficeResult']['weeklyBoxOfficeList']:
            context = {
                'title' : rec['movieNm'],
                'rank' : rec['rank'],
                'rank_inten' : rec['rankInten'],
            }

            movie = BoxofficeMovie.objects.create(**context)
            movie.save()