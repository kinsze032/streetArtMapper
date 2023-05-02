from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3, label="Znajdź")
    search_in = forms.ChoiceField(
        required=False,
        choices=(
            ("title", "Tytuł"),
            ("location__city", "Miasto"),
            ("category__type", "Typ"),
        ),
        label="Szukaj w ",
        initial="category__type",
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
        exclude = ["date_created", "date_edited", "art", "creator"]
        labels = {
            "content": _("Treść recenzji"),
            "rating": _("Ocena"),
        }

    rating = forms.IntegerField(min_value=0, max_value=5)
