from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'release_year',
            'genre',
            'rating',
            'running_time',
            'content',
            'director',
            'actors',
        ]

        labels = {
            'title': '영화 제목',
            'release_year': '개봉 년도',
            'genre': '장르',
            'rating': '별점',
            'running_time': '러닝타임',
            'content': '리뷰 내용',
            'director': '감독',
            'actors': '주연',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '영화 제목을 입력하세요'}),
            'release_year': forms.NumberInput(attrs={'placeholder': '예: 2024'}),
            'genre': forms.TextInput(attrs={'placeholder': '예: 액션, 코미디, SF'}),
            'rating': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '5',
                'placeholder': '예: 4.5'
            }),
            'running_time': forms.NumberInput(attrs={'placeholder': '분 단위로 입력'}),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': '리뷰 내용을 입력하세요'
            }),
            'director': forms.TextInput(attrs={'placeholder': '감독 이름'}),
            'actors': forms.TextInput(attrs={'placeholder': '주연 배우'}),
        }