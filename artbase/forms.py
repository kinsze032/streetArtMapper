from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review, StreetArt


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3, label="Znajdź")
    search_in = forms.ChoiceField(
        required=False,
        choices=(
            ("category__type", "Typ"),
            ("title", "Tytuł"),
            ("location__city", "Miasto"),
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


# class CreateStreetArtForm(forms.ModelForm):
#     class Meta:
#         model = StreetArt
#         fields = ['title', 'artist', 'year', 'description', 'category']
#         labels = {
#             'title': _("Tytuł"),
#             'artist': _("Artysta"),
#             'year': _("Rok utworzenia"),
#             'description': _("Opis"),
#             'category': _("Kategoria"),
#         }
#         widgets = {
#             'longitude': forms.HiddenInput(),
#             'latitude': forms.HiddenInput(),
#         }
#
#     year = forms.IntegerField(min_value=2000, max_value=2999)
#     longitude = forms.DecimalField(widget=forms.HiddenInput())
#     latitude = forms.DecimalField(widget=forms.HiddenInput())
#
#
# class EditStreetArtForm(forms.ModelForm):
#     class Meta:
#         model = StreetArt
#         fields = ['title', 'artist', 'year', 'description', 'category']
#         labels = {
#             'title': _("Tytuł"),
#             'artist': _("Artysta"),
#             'year': _("Rok utworzenia"),
#             'description': _("Opis"),
#             'category': _("Kategoria"),
#         }
#
#     year = forms.IntegerField(min_value=2000, max_value=2999)

# PONIŻEJ SKRÓCONA WERSJA POWYŻSZYCH DWÓCH KLAS


class StreetArtFormBase(forms.ModelForm):
    class Meta:
        model = StreetArt
        fields = ["title", "artist", "year", "description", "category"]
        labels = {
            "title": _("Tytuł"),
            "artist": _("Artysta"),
            "year": _("Rok utworzenia"),
            "description": _("Opis"),
            "category": _("Kategoria"),
        }

    year = forms.IntegerField(min_value=2000, max_value=2999)


class CreateStreetArtForm(StreetArtFormBase):
    class Meta(StreetArtFormBase.Meta):
        widgets = {
            "longitude": forms.HiddenInput(),
            "latitude": forms.HiddenInput(),
        }

    longitude = forms.DecimalField(widget=forms.HiddenInput())
    latitude = forms.DecimalField(widget=forms.HiddenInput())


class EditStreetArtForm(StreetArtFormBase):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "username", "style": "font-size: 13px;"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "password", "style": "font-size: 13px;"}
        )
    )
