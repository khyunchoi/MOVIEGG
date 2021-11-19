import json
import time
from django.conf.urls import url
from django.http.request import QueryDict
import requests
from .models import BoxofficeMovie, Genre, Movie, Actor
from django.shortcuts import render
from django.forms.models import model_to_dict
from ast import literal_eval

# Create your views here.
def load(request):
    # json 데이터를 파일을 만들기 위해서 가져오는 과정
    rank_now = int(time.strftime('%Y%m%d'))-7
    url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=722013d232df9db0ef7e9631ebafdc3b&targetDt={rank_now}&weekGb=0'
    res = requests.get(url)
    text = res.text
    d = json.loads(text)
    with open('movierank.json', 'w', encoding="UTF-8", ) as p:
        json.dump(d, p, ensure_ascii=False, indent=4)

    # json 데이터를 불러와서 파싱하는과정
    with open("./movierank.json", "r", encoding='UTF8') as json_file:
        json_data = json.loads(json_file.read())

        for rec in json_data['boxOfficeResult']['weeklyBoxOfficeList']:
            context = {
                'title' : rec['movieNm'],
                'rank' : rec['rank'],
                'rank_inten' : rec['rankInten'],
            }
            
            movie = BoxofficeMovie.objects.get_or_create(**context)


    movies = list(BoxofficeMovie.objects.values())
    print(movies)
    context = {
        'movies' : movies
    }

        
    return render(request, 'movies/load.html', context)

def movieupdate(request):
    # for i in range(1,500):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR&page={1}'
    res = requests.get(url)
    text = res.text
    d = json.loads(text)
    with open('movieupdate.json', 'w', encoding="UTF-8", ) as p:
        json.dump(d, p, ensure_ascii=False, indent=4)

    # json 데이터를 불러와서 파싱하는과정
    with open("./movieupdate.json", "r", encoding='UTF8') as json_file:
        json_data = json.loads(json_file.read())


        for rec in json_data['results']:
            movie_id = rec['id']

            # 런타임을 받아오기위한 movie detail 로의 접근
            runtime_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR'
            runtime = requests.get(runtime_url)
            runtime_text = runtime.json()
            
            # 감독을 받아오기위한 movie credit 으로의 접근
            director_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR'
            director = requests.get(director_url)
            director_text = director.json()
            crew = director_text['crew']
            cast = director_text['cast']
            for direc in crew:
                if direc['job'] == 'Director':
                    director = direc['original_name']
            # for actor in 
            if type(director) != str:
                director = 'unknown'
            
                    
            # print(cast)
            # print(director_text['crew'])
            # if director_text['crew']['job'] == 'Driector':
            #     director_name = director_text['crew']['original_name']
            # print(director_name)

            

            showtime = runtime_text['runtime']
            overview = runtime_text['overview']
            context ={
                'movie_code' : rec['id'],
                'title' : rec['title'],
                'release_date' : rec['release_date'],
                'plot' : overview,
                'poster_path' : rec['poster_path'],
                'showtime' : showtime,
                'director' : director,
            }
            
            movie = Movie.objects.get_or_create(**context)

            for i in range(2):
                if len(cast):
                    context = {
                        'movie_code' : movie_id,
                        'name' : cast[i]['name'] 
                    }
                    actor = Actor.objects.get_or_create(name=cast[i]['name'])
                    actor = Actor.objects.get(name=cast[i]['name'])
                    movie = Movie.objects.get(movie_code=rec['id'])
                    movie.movie_actor.add(actor)
                    # actor.movie_code.add(movie) 해도 똑같이 만들어짐
                    # 중계테이블을 이용해서 참조/ 역참조 관계를 잘 만들어야함.
                    # html으로 가져다 쓰고싶으면 for actor in movie.moive_actor :
            
            genres = rec['genre_ids']
            for genre in genres:
                genre = Genre.objects.get(genre_num=genre)
                movie = Movie.objects.get(movie_code=rec['id'])
                genre.movie_genre.add(movie)
            

    # movies = list(Movie.objects.values())
    movies = Movie.objects.all()
    context = {
        'movies' : movies
    }


    
    return render(request, 'movies/update.html', context)

def genreupdate(request):
    url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR'
    res = requests.get(url)
    text = res.text
    d = json.loads(text)
    with open('genreupdate.json', 'w', encoding="UTF-8", ) as p:
        json.dump(d, p, ensure_ascii=False, indent=4)
    
    # json 데이터를 불러와서 파싱하는과정
    with open("./genreupdate.json", "r", encoding='UTF8') as json_file:
        json_data = json.loads(json_file.read())

        for rec in json_data['genres']:
            context ={
                'name' : rec['name'],
                'genre_num' : rec['id'],
            }

            genre = Genre.objects.get_or_create(**context)
    genres = list(Genre.objects.values())
    context = {
        'genres' : genres
    }

    return render(request, 'movies/genreupdate.html' , context)