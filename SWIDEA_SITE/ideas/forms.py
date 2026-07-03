from django import forms
from .models import Idea, DevTool

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["title", "image", "content", "interest", "devtool"]

        labels = {
            "title": "아이디어명",
            "image": "이미지",
            "content": "아이디어 설명",
            "interest": "관심도",
            "devtool": "개발툴",
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "interest": forms.NumberInput(attrs={"class": "form-control"}),
            "devtool": forms.Select(attrs={"class": "form-control"}),
        }


class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ["name", "kind", "content"]

        labels = {
            "name": "이름",
            "kind": "종류",
            "content": "설명",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "kind": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }