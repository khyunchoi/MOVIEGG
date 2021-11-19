from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, ReviewComment
from .forms import ReviewForm, ReviewCommentForm

# Create your views here.
def index(request):
    context = {

    }
    return render(request, 'articles/index.html', context)


def review(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'articles/review.html', context)


def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('articles:review') # 임시
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
            return redirect('articles:review') # 임시
    else:
        form = ReviewForm()
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