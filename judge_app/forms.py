from django import forms

from .models import Project

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.project_id

class ScoreForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'errors'

    judge_id = forms.CharField(label=None, max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Judge ID'}))
    award_code = forms.CharField(label=None, max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Award Code'}))
    #project_id = forms.CharField(label=None, max_length=50,
    #    widget=forms.TextInput(attrs={'placeholder':'Project ID'}))
    project_id = MyModelChoiceField(label=None,
        queryset=Project.objects.all(),
        to_field_name='project_id',
        empty_label="Project ID")
    score = forms.IntegerField(label=None, min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'placeholder':'Score'}))

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        #choices = [(x.pk, x.project_id) for x in Project.objects.all()]
        #self.fields['project_id'].choices = choices
        #self.fields['project_id'].choices.append(("Project ID", "Project ID"))
    
    def clean(self):
        cleaned_data = super(ScoreForm, self).clean()
        try:
            selected = cleaned_data.get('project_id')
            project = Project.objects.get(\
                project_id=selected.project_id)
            if project.award_code != cleaned_data.get('award_code'):
                msg = "Project ID not associated with award code."
                self.add_error("award_code",msg)
        except (Project.DoesNotExist, ValueError, AttributeError):
            msg = "Project ID does not exist."
            self.add_error("project_id", msg)
