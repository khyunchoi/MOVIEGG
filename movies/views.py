import json
import time
from django.conf.urls import url
from django.http.request import QueryDict
from django.http.response import JsonResponse
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from .models import BoxofficeMovie, Character, Genre, Movie, Actor, Question
from django.shortcuts import render
from django.forms.models import model_to_dict
from ast import literal_eval
from django.db.models import Q

# Create your views here.
def movie_detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)


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

    # 이맘때쯤 유행했던 영화에 관해...
    # 근데 최근 3년정도의 1위를 뽑아내야 되기 때문에
    imgsrc = []
    for i in range(1,4):
        rank_latest = int(time.strftime('%Y%m'))-100 * i
        url = f'https://movie.daum.net/ranking/boxoffice/monthly?date={rank_latest}'
        
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            imgsrc.append(str(soup.select_one('#mainContent > div > div.box_boxoffice > ol > li:nth-child(1) > div > div.thumb_item > div.poster_movie > img')))
            
        else: 
            print(response.status_code)


    # 당신에게 추천하는 영화의 알고리즘
    # DB 에서 평점이 가장 높은 영화를 뽑을꺼야~ 3개!
    # -> DB에서뽑지말고 api를 활용해서 최상층 3개를 가져와도됨~
    # 로그인 했을경우 사용자가 줬던 가장 높은 평점의 영화나 리뷰작성 영화를 고르고
    #  similler api이용

    #로그인 안했을 경우
    movies = Movie.objects.all().order_by('-vote_average')
    recimg = []
    for k in range(3) :
        recimg.append(movies[k].poster_path)
    

     
    movies = list(BoxofficeMovie.objects.values())
    context = {
        'movies' : movies,
        'imgsrc' : imgsrc,
        'recimg' : recimg,
    }

        
    return render(request, 'movies/load.html', context)

def movieupdate(request):
    for i in range(1,20):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR&page={i}'
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
                    'vote_average' :  rec['vote_average']
                }
                if not rec['release_date']:
                    context['release_date'] = '9999-09-09'
                movie = Movie.objects.get_or_create(**context)
                if len(cast) > 2:
                    for i in range(3):
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
                else:
                    for i in range(len(cast)):
                        context = {
                            'movie_code' : movie_id,
                            'name' : cast[i]['name'] 
                        }
                        actor = Actor.objects.get_or_create(name=cast[i]['name'])
                        actor = Actor.objects.get(name=cast[i]['name'])
                        movie = Movie.objects.get(movie_code=rec['id'])
                        movie.movie_actor.add(actor)
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

def leagueoflegend(request):
    
    with open("./leagueofcharacter.json", "r", encoding='UTF8') as json_file:
        json_data = json.loads(json_file.read())

        for rec in json_data['character']:
            context ={
                'character_number' : rec['character_number'],
                'name' : rec['name'],
                'eng_name' : rec['eng_name']
            }
            character = Character.objects.get_or_create(**context)
    return render(request, 'movies/temp.html')





def lol_recommend(request):
    # 질문지 1번을 꺼내올거야~
    questions = list(Question.objects.values())
    context ={
        'questions' : questions,
    }
    return JsonResponse(context)

    # if i < 32:
    #     question_a,question_b = questions[i].content.split('vs')
    #     context = {
    #         'question_a' : question_a,
    #         'question_b' : question_b,
    #         'i' : i,
    #         'double_i' : i*2,
    #         'double_extra_i' : i*2+1,
    #     }
    
    #     return render(request, 'movies/lolrec.html', context)

    # else:
    #     character = Character.objects.get(number=i)
    #     context = {
    #         'character': character
    #     }
        
    #     return render(request, 'movies/lolresult.html', context)


def lol_reccomend_start(request):
    return render(request, 'movies/lolrecstart.html')

def lol_result(request, i):
    character = Character.objects.get(character_number=i)
    character_genre = character.genre.all()
    max = 0
    recolist = []
    recogenre = []
    reco_imglist = []
    reco_imgfinal = {}
    plz = Movie.objects.filter(genre=19)
    print(plz)
    for genre in character_genre:
        recogenre.append(genre)
        print(genre)
        movies = Movie.objects.filter(genre=genre).order_by('-vote_average')
        
        # genre_recommend = Movie.objects.filter(genre=genre).order_by('-vote_average')[0:3]
        if not genre.genre_num == 16:
            genre_recommend = Movie.objects.filter(genre=genre).order_by('-vote_average').filter(~Q(genre=3))[0:3]
            print(genre_recommend)
            if len(genre_recommend) < 3:
                genre_empty = (Movie.objects.filter(genre=genre).order_by('-vote_average').filter(genre=3)[0:3-len(genre_recommend)])
                for reco in genre_empty:
                    recolist.append(reco.movie_code)
        else:
            genre_recommend = Movie.objects.filter(genre=genre).order_by('-vote_average')[0:3]
        if max < movies[0].vote_average:
            max = movies[0].vote_average
            movie_one = movies[0]
        print(genre_recommend)
        
        for reco in genre_recommend:
            recolist.append(reco.movie_code)
        print(recolist)
            
    # 추천 영화를 가져오는 접근!!
    for reco in recolist:
        recommend_url = f'https://api.themoviedb.org/3/movie/{reco}?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR'
        recommend = requests.get(recommend_url)
        recommend_img = recommend.json()
        reco_img = recommend_img['poster_path']
        reco_imglist.append(reco_img)
    for i in range(3):
        reco_imgfinal[i] = reco_imglist[i*3:(i+1)*3]
    reco_image1 = reco_imgfinal[0]
    reco_image2 = reco_imgfinal[1]
    reco_image3 = reco_imgfinal[2]
        

 



    
    
    # 영화의 overview를 받아오기 위한 접근
    overview_url = f'https://api.themoviedb.org/3/movie/{movie_one.movie_code}?api_key=f66a306bb52bff7bbc064b3b796172b2&language=ko-KR'
    movie_overviews = requests.get(overview_url)
    movie_overviews_text = movie_overviews.json()

    movie_overview = movie_overviews_text['overview']


    url = f'https://www.leagueoflegends.com/ko-kr/champions/{character.eng_name}'
    # 롤 홈페이지에서 정보들 가져와!!
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content.decode('utf-8','replace')
        # html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        image = str(soup.select_one('#gatsby-focus-wrapper > div > section.style__Wrapper-sc-8gkpub-30.hvTntU > div.style__SectionInner-sc-8gkpub-3.drSgts > div.style__ForegroundAsset-sc-8gkpub-4.fyyYJz > img'))
        overview = str(soup.select_one('#gatsby-focus-wrapper > div > section.style__Wrapper-sc-8gkpub-30.hvTntU > div.style__SectionInner-sc-8gkpub-3.drSgts > div.style__Dock-sc-8gkpub-5.eVSOFq > div.style__Info-sc-8gkpub-7.kTzPTF > div.style__Desc-sc-8gkpub-9.efkwqI > p').text)
        final_overview = overview.replace(str(soup.select_one('#gatsby-focus-wrapper > div > section.style__Wrapper-sc-8gkpub-30.hvTntU > div.style__SectionInner-sc-8gkpub-3.drSgts > div.style__Dock-sc-8gkpub-5.eVSOFq > div.style__Info-sc-8gkpub-7.kTzPTF > div.style__Desc-sc-8gkpub-9.efkwqI > p > button').text),"")
        thumbnail = str(soup.select_one('#gatsby-focus-wrapper > div > section.style__Wrapper-sc-8gkpub-30.hvTntU > div.style__SectionInner-sc-8gkpub-3.drSgts > div.style__Dock-sc-8gkpub-5.eVSOFq > div.style__Name-sc-8gkpub-6.kajbWl > div > h1 > span > div > span'))
    else:
        print(response.status_code)
    
    context = {
        'character' : character,
        'image' : image,
        'overview' :final_overview,
        'thumbnail' :thumbnail,
        'movie' :movie_one,     
        'movie_overview' : movie_overview,
        'recogenre' : recogenre,
        'raco_image1' :reco_image1,
        'raco_image2' :reco_image2,
        'raco_image3' :reco_image3,
    }



    
    return render(request, 'movies/lolresult.html', context)