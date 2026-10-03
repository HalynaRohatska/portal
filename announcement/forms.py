from django import forms

from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content", "is_pinned", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Заголовок оголошення",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Текст оголошення",
            }),
            "is_pinned": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError(
                "Заголовок повинен містити щонайменше 3 символи."
            )
        return title

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if len(content) < 10:
            raise forms.ValidationError(
                "Текст оголошення повинен містити щонайменше 10 символів."
            )
        return content