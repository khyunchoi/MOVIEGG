from django import forms
from .models import Review, ReviewComment, FreeBoard, FreeComment


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'content', 'grade']


class ReviewCommentForm(forms.ModelForm):

    class Meta:
        model = ReviewComment
        fields = ['content']


class FreeBoardForm(forms.ModelForm):

    class Meta:
        model = FreeBoard
        fields = ['title', 'content', 'image']


class FreeCommentForm(forms.ModelForm):

    class Meta:
        model = FreeComment
        fields = ['content']
