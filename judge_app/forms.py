from django import forms

class ScoreForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'errors'

    judge_id = forms.CharField(label=None, max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Judge ID'}))
    award_id = forms.CharField(label=None, max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Award ID'}))
    project_id = forms.CharField(label=None, max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Project ID'}))
    score = forms.IntegerField(label=None, min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'placeholder':'Score'}))
