from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Project,
    #Judge,
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

    #judge_id = forms.CharField(max_length=255, help_text="Judge No.")
    score = forms.IntegerField(max_value=100, min_value=0, help_text="Score")
    class Meta:
        model = JudgingResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['judge_id'].widget.attrs['autofocus'] = u'autofocus'
        self.fields['project'].queryset = Project.objects.order_by('project_id')
        self.fields.get('project').empty_label = "Project ID"
        self.fields.get('award').empty_label = "Category Code"
         
    def clean(self):
        cleaned_data = super(ScoreForm, self).clean()
        """
        try:
            judge_id = self.cleaned_data.get('judge_id')
            judge = Judge.objects.get(judge_id=judge_id)
            self.instance.judge_id = judge
        except Judge.DoesNotExist:
            msg = "Invalid Judge ID."
            self.add_error("judge_id", msg)
            return
        """
        try:
            project = cleaned_data.get('project')
            award = cleaned_data.get('award')
            if not self.is_valid_result_count(award):
                msg = "Juding for award '{0}' already complete.".format(award)
                self.add_error("award", msg)
            if award not in project.awards.all() and award:
                msg = "{1} not associated with {0}.".format(award, project) 
                self.add_error("award", msg)
            #if award not in self.instance.judge_id.awards.all() \
            #    and award:
            #    msg = "{1} not associated with {0}.".format(award, judge) 
            #    self.add_error("award", msg)
        except (Project.DoesNotExist, ValueError, AttributeError):
            msg = "Project ID does not exist."
            self.add_error("project", msg)

    def is_valid_result_count(self, award):
        judges = award.number_of_judges
        total = Award.objects.filter(code=award.code,
            projects__isnull=False).count() * award.number_of_judges
        results = JudgingResult.objects.filter(award=award.code)
        if results.count() >= total:
            return False
        return True
