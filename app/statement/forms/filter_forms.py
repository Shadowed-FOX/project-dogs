from django import forms
from statement.models import Dog, City

class FilterForm(forms.Form):
    voivodeship = forms.ChoiceField(
        choices=[],
        required=False,
        label="Województwo"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="Miasto"
    )
    size = forms.ChoiceField(
        choices=[("", "Wszystkie rozmiary")] + Dog.SIZE_CHOICES,
        required=False,
        label="Rozmiar"
    )
    race = forms.CharField(
        required=False,
        label="Rasa",
        widget=forms.TextInput(attrs={'placeholder' : 'np. owczarek'})
    )

    name = forms.CharField(
        required=False,
        label="Imię",
        widget=forms.TextInput(attrs={'placeholder' : 'Wpisz imię'})
    )

    class Meta:
        model = Dog
        fields = ['voivodeship', 'city', 'size', 'race', 'name']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        voivodeships = City.objects.order_by().values_list("voivodeship", flat=True).distinct()
        self.fields['voivodeship'].choices = [("", "Wybierz województwo")] + [(v, v) for v in voivodeships]
        self.fields['city'].widget.attrs.update({'style': 'width: 180px'})
        self.fields['voivodeship'].widget.attrs.update({'style' : 'width: 180px'})


        if 'voivodeship' in self.data:
            self.fields['city'].queryset = City.objects.filter(voivodeship=self.data.get('voivodeship')).order_by('city')
        elif self.initial.get('vivodeship'):
            self.fields['city'].queryset = City.objects.filter(voivodeships=self.initial['voivodeship']).order_by('city')