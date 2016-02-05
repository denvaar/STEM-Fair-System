from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import ScoreForm

class ScoreSubmissionView(FormView):
    template_name = 'score-submit.html'
    form_class = ScoreForm
    success_url = 'score-submit.html'

    def form_valid(self, form):
        # Called when the valid form data has been POSTed.
        # TODO: update models here.
        print form.cleaned_data
        return super(ScoreSubmissionView, self).form_valid(form)
