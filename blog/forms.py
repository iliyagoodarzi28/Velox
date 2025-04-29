# forms.py
from django import forms
from .models import Comment , Rating

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']



class BlogFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('most_viewed', 'Most visited'),
        ('latest', 'Newest'),
        ('oldest', 'Oldest'),
        ('lowest_rating', 'Lowest score'),
        ('highest_rating', 'Most score'),
        
    ]
    
    filter_by = forms.ChoiceField(choices=FILTER_CHOICES, label="Blog Filter")


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 6)])  # انتخاب امتیاز از 1 تا 5
        }        