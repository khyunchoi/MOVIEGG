from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.core.paginator import Paginator
from .models import Review, ReviewComment, FreeBoard, FreeComment
from .forms import ReviewForm, ReviewCommentForm, FreeBoardForm, FreeCommentForm

# Create your views here.
def index(request):
    context = {

    }
    return render(request, 'articles/index.html', context)


def review(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 8)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'articles/review.html', context)


def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('articles:review_detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/review_create.html', context)


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


def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
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


def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review.delete()
    return redirect('articles:review')


def review_comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = ReviewCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('articles:review_detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.reviewcomment_set.all(),
    }
    return render(request, 'articles/review_detail.html', context)


def review_comment_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(ReviewComment, pk=comment_pk)
    comment.delete()
    return redirect('articles:review_detail', review.pk)


def freeboard(request):
    freeboards = FreeBoard.objects.order_by('-pk')
    paginator = Paginator(freeboards, 8)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'articles/freeboard.html', context)


def freeboard_create(request):
    if request.method == 'POST':
        form = FreeBoardForm(request.POST, request.FILES)
        if form.is_valid():
            freeboard = form.save(commit=False)
            freeboard.user = request.user
            freeboard.save()
            return redirect('articles:freeboard') # 임시
    else:
        form = FreeBoardForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/freeboard_create.html', context)


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


def freeboard_update(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    if request.method == 'POST':
        form = FreeBoardForm(request.POST, request.FILES, instance=freeboard)
        if form.is_valid():
            form.save()
            return redirect('articles:freeboard') # 임시
    else:
        form = FreeBoardForm(instance=freeboard)
    context = {
        'freeboard': freeboard,
        'form': form,
    }
    return render(request, 'articles/freeboard_update.html', context)


def freeboard_delete(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    freeboard.delete()
    return redirect('articles:freeboard')


def free_comment_create(request, freeboard_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    comment_form = FreeCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.free_board = freeboard
        comment.user = request.user
        comment.save()
        return redirect('articles:freeboard_detail', freeboard.pk)
    context = {
        'comment_form': comment_form,
        'freeboard': freeboard,
        'comments': freeboard.freecomment_set.all(),
    }
    return render(request, 'articles/freeboard_detail.html', context)


def free_comment_delete(request, freeboard_pk, comment_pk):
    freeboard = get_object_or_404(FreeBoard, pk=freeboard_pk)
    comment = get_object_or_404(FreeComment, pk=comment_pk)
    comment.delete()
    return redirect('articles:freeboard_detail', freeboard.pk)