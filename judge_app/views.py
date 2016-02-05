from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .forms import ScoreForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # TODO: Add any needed context data here.
        return context

class ScoreSubmissionView(FormView):
    template_name = 'score-submit.html'
    form_class = ScoreForm
    success_url = 'score-submit.html'

    def form_valid(self, form):
        print dir(self)
        # Called when the valid form data has been POSTed.
        # TODO: update models here.
        messages.success(self.request,
            "Thank you! Score recorded successfully.")
        print form.cleaned_data
        return super(ScoreSubmissionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
            "Error trying to record score.")
        return super(ScoreSubmissionView, self).form_invalid(form)
