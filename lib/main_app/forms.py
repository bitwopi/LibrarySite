from django import forms

from main_app.models import Genre


class FilterForm(forms.Form):
    genres = forms.ModelChoiceField(label="Жанры", required=False, queryset=Genre.objects.all())
    pages = forms.IntegerField(label="Количество страниц", required=False)
    cost = forms.FloatField(label="Залог", required=False)

    class Meta:
        fields = [
            'genres',
            'pages',
            'cost',
        ]

