from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Review, ReviewComment, FreeBoard, FreeComment
from .forms import ReviewForm, ReviewCommentForm, FreeBoardForm, FreeCommentForm
from movies.models import Movie
from django.db.models import Q

# Create your views here.
@require_safe
def index(request):
    # 평점 기준으로 영화를 정렬해서 애니메이션 제외 top5 선정
    movies = Movie.objects.order_by('-vote_average')

    top_movies = []
    for movie in movies:
        if len(top_movies) < 5:
            for genre in movie.genre.all():
                if genre.name == '애니메이션':
                    break
            else:
                top_movies.append(movie)
        else:
            break
    
    # 추천수 기준으로 top5 리뷰 선정
    reviews = Review.objects.all()

    top_reviews = []
    for review in reviews:
        top_reviews.append([review.like_users.count(), review])
    top_reviews.sort(key=lambda x:x[0], reverse=True)
    top_reviews = top_reviews[:5]

    context = {
        'top_movies': top_movies,
        'top_reviews': top_reviews,
    }
    return render(request, 'articles/index.html', context)


@require_safe
def review(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 6)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_number': int(page_number),
        'page_obj': page_obj,
    }
    return render(request, 'articles/review.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def review_create(request, movie_pk):
    if request.user.exp < 500:
        return redirect('articles:index')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = Movie.objects.get(pk=movie_pk)
            review.save()
            review.user.exp += 50
            review.user.save()
            return redirect('articles:review_detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/review_create.html', context)


@require_safe
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.reviewcomment_set.all()
    comment_form = ReviewCommentForm()
    context = {
        'review': review,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/review_detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user != review.user:
        return redirect('articles:review_detail', review.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('articles:review_detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'articles/review_update.html', context)

@require_POST
def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
    return redirect('articles:review')


def review_like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)

        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
            liked = False
        else:
            review.like_users.add(request.user)
            liked = True
        
        like_count = review.like_users.count()
        context = {
            'liked': liked,
            'like_count': like_count,
        }
        
        return JsonResponse(context)


@login_required
@require_http_methods(['GET', 'POST'])
def review_comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = ReviewCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        comment.user.exp += 20
        comment.user.save()
        return redirect('articles:review_detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.reviewcomment_set.all(),
    }
    return render(request, 'articles/review_detail.html', context)


@require_POST
def review_comment_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(ReviewComment, pk=comment_pk)
    if request.user.is_authenticated:
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:review_detail', review.pk)


@require_safe
def freeboard(request):
    freeboards = FreeBoard.objects.order_by('-pk')
    paginator = Paginator(freeboards, 12)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    n = len(freeboards)
    if n % 12 == 0:
        n = range(0)
    else:
        n = range(12 - n % 12)

    context = {
        'n' : n,
        'page_number': int(page_number),
        'page_obj': page_obj,
    }
    return render(request, 'articles/freeboard.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def freeboard_create(request):
    if request.method == 'POST':
        form = FreeBoardForm(request.POST, request.FILES)
        if form.is_valid():
            freeboard = form.save(commit=False)
            freeboard.user = request.user
            freeboard.save()
            freeboard.user.exp += 50
            freeboard.user.save()
            return redirect('articles:freeboard_detail', freeboard.pk)
    else:
        form = FreeBoardForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/freeboard_create.html', context)


@require_safe
def freeboard_detail(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    comments = freeboard.freecomment_set.all()
    comment_form = FreeCommentForm()
    context = {
        'freeboard': freeboard,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/freeboard_detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def freeboard_update(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    if request.user != freeboard.user:
        return redirect('articles:freeboard_detail', freeboard.pk)

    if request.method == 'POST':
        form = FreeBoardForm(request.POST, request.FILES, instance=freeboard)
        if form.is_valid():
            form.save()
            return redirect('articles:freeboard_detail', freeboard.pk)
    else:
        form = FreeBoardForm(instance=freeboard)
    context = {
        'freeboard': freeboard,
        'form': form,
    }
    return render(request, 'articles/freeboard_update.html', context)


@require_POST
def freeboard_delete(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    if request.user.is_authenticated:
        if request.user == freeboard.user:
            freeboard.delete()
    return redirect('articles:freeboard')


def freeboard_like(request, freeboard_pk):
    if request.user.is_authenticated:
        freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)

        if freeboard.like_users.filter(pk=request.user.pk).exists():
            freeboard.like_users.remove(request.user)
            liked = False
        else:
            freeboard.like_users.add(request.user)
            liked = True
        
        like_count = freeboard.like_users.count()
        context = {
            'liked': liked,
            'like_count': like_count,
        }
        
        return JsonResponse(context)


@login_required
@require_http_methods(['GET', 'POST'])
def free_comment_create(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    comment_form = FreeCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.free_board = freeboard
        comment.user = request.user
        comment.save()
        comment.user.exp += 20
        comment.user.save()
        return redirect('articles:freeboard_detail', freeboard.pk)
    context = {
        'comment_form': comment_form,
        'freeboard': freeboard,
        'comments': freeboard.freecomment_set.all(),
    }
    return render(request, 'articles/freeboard_detail.html', context)


@require_POST
def free_comment_delete(request, freeboard_pk, comment_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    comment = get_object_or_404(FreeComment, pk=comment_pk)
    if request.user.is_authenticated:
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:freeboard_detail', freeboard.pk)


@require_safe
def search(request):
    word = request.GET.get('word')
    movies = Movie.objects.filter(Q(title__icontains=word) | Q(plot__icontains=word))
    reviews = Review.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))
    freeboards = FreeBoard.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))

    context = {
        'movies': movies,
        'reviews': reviews,
        'freeboards': freeboards,
    }
    return render(request, 'articles/search.html', context)


@require_safe
def search_movie(request):
    context = {

    }
    return render(request, 'articles/search_movie.html', context)