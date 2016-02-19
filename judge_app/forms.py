from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Project,
    Judge,
    Award,
    JudgingResult,
)


class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.project_id


class AwardChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.code

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super(BaseModelForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.help_text
                })


class ScoreForm(BaseModelForm):
    error_css_class = 'errors'
    required_css_class = 'errors'

    judge_id = forms.CharField(max_length=255, help_text="Judge ID")
    score = forms.IntegerField(max_value=100, min_value=0, help_text="Score")

    class Meta:
        model = JudgingResult
        exclude = ('judge_id',)
   
    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields.get('project').empty_label = "Project ID"
        self.fields.get('award').empty_label = "Award ID"
         
    def clean(self):
        cleaned_data = super(ScoreForm, self).clean()
        try:
            judge_id = self.cleaned_data.get('judge_id')
            judge = Judge.objects.get(judge_id=judge_id)
            self.instance.judge_id = judge
        except Judge.DoesNotExist:
            msg = "Invalid Judge ID."
            self.add_error("judge_id", msg)
            return
        try:
            project = cleaned_data.get('project')
            award = cleaned_data.get('award')
            if award not in project.awards.all() and award:
                msg = "{1} not associated with {0}.".format(award, project) 
                self.add_error("award", msg)
            if award not in self.instance.judge_id.awards.all() \
                and award:
                msg = "{1} not associated with {0}.".format(award, judge) 
                self.add_error("award", msg)
        except (Project.DoesNotExist, ValueError, AttributeError):
            msg = "Project ID does not exist."
            self.add_error("project", msg)

