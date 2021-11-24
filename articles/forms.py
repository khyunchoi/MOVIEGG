from django import forms
from .models import Review, ReviewComment, FreeBoard, FreeComment
from .widgets import starWidget


class ReviewForm(forms.ModelForm):

    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'review-title',
                'placeholder': '제목',
            }
        ),
    )

    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'review-content',
            }
        ),
    )

    class Meta:
        model = Review
        fields = ['title', 'content', 'grade']
        widgets = {
            'grade': starWidget,
        }
        labels = {
            'grade': "평점",
        }


class ReviewCommentForm(forms.ModelForm):

    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'review-comment',
                'placeholder': '댓글을 입력하세요.',
            }
        ),
    )

    class Meta:
        model = ReviewComment
        fields = ['content']


class FreeBoardForm(forms.ModelForm):

    title = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'freeboard-title',
                'placeholder': '제목',
            }
        ),
    )

    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'freeboard-content',
            }
        ),
    )

    class Meta:
        model = FreeBoard
        fields = ['title', 'content', 'image']


class FreeCommentForm(forms.ModelForm):

    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'freeboard-comment',
                'placeholder': '댓글을 입력하세요.',
            }
        ),
    )

    class Meta:
        model = FreeComment
        fields = ['content']
