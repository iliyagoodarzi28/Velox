# forms.py
from django import forms
from .models import Color, Size



class ShoeSelectionForm(forms.Form):
    color = forms.ModelChoiceField(
        queryset=Color.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1, required=True, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        shoe = kwargs.pop('shoe', None)
        super().__init__(*args, **kwargs)
        if shoe:
            self.fields['color'].queryset = shoe.colors.all()
            self.fields['size'].queryset = shoe.sizes.all()

