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

    def get_context_data(self, **kwargs):
        context = super(ScoreSubmissionView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Called when the valid form data has been POSTed.
        messages.success(self.request,
            "Thank you! Score recorded successfully.")
        return super(ScoreSubmissionView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ScoreSubmissionView, self).form_invalid(form)
