from django import forms

from .models import (
    Project,
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

    class Meta:
        model = JudgingResult
        fields = '__all__'
   
    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields.get('project').empty_label = "Project ID"
        self.fields.get('award').empty_label = "Award ID"
    
    def clean(self):
        cleaned_data = super(ScoreForm, self).clean()
        try:
            project = cleaned_data.get('project')
            award = cleaned_data.get('award')
            if award not in project.awards.all():
                msg = "Project ID not associated with Award ID."
                self.add_error("award", msg)
                
        except (Project.DoesNotExist, ValueError, AttributeError):
            msg = "Project ID does not exist."
            self.add_error("project", msg)
            print dir(self)

