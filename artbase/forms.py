from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3, label="Znajdź")
    search_in = forms.ChoiceField(
        required=False,
        choices=(
            ('title', "Tytuł"),
            ('location__city', 'Miasto'),
            ('category__type', 'Typ'),
        ),
        label="Szukaj w ",
        initial='location__city',
    )
