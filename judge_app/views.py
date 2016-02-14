import operator
from itertools import groupby

from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .forms import ScoreForm
from .models import (
    Award,
    JudgingResult,
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # TODO: Add any needed context data here.
        return context


class ScoreSubmissionView(CreateView):
    template_name = 'score-submit.html'
    form_class = ScoreForm
    success_url = 'score-submit.html'

    def get_context_data(self, **kwargs):
        context = super(ScoreSubmissionView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Called when the valid form data has been POSTed.
        fv = super(ScoreSubmissionView, self).form_valid(form)
        award_id = form.data['award']
        self.get_award_results(award_id)
        messages.success(self.request,
            "Thank you! Score recorded successfully.")
        return fv

    def form_invalid(self, form):
        return super(ScoreSubmissionView, self).form_invalid(form)

    def get_award_results(self, award_id):
        total = Award.objects.filter(code=award_id,
            projects__isnull=False).count() * 3
        results = JudgingResult.objects.filter(award=award_id)
        print results.count(), "/", total
        if results.count() < total:
            return
        raw_scores = {}
        judge_scores = {}
        for r in results.all():
            try:
                judge_scores[r.judge_id].append((r.project,r.score))
            except KeyError:
                judge_scores[r.judge_id] = [(r.project,r.score)]
            try:
                raw_scores[r.project] = raw_scores[r.project] + r.score
            except KeyError:
                raw_scores[r.project] = r.score
        raw_scores = dict([(k,v/300.0) for k,v in raw_scores.iteritems()])
        print raw_scores
        print judge_scores
        # sort each judge's scores for each project
        for j in judge_scores.items():
            for p in j[1]:
                j[1].sort(key=operator.itemgetter(1), reverse=True)
        print "\nsorted", judge_scores
        
        # rank the scores.
        ranked_scores = {}
        for j in judge_scores.items():
            rankings = []
            rank = 1
            for k,v in groupby(j[1], lambda x: x[1]):
                grp = [(rank, tup[0]) for tup in v]
                rankings += grp
                rank += len(grp)
            ranked_scores[j[0]] = rankings        
        print "\nranked", ranked_scores

        # Sum the ranks for each project.
        x = [t for sub in ranked_scores.values() for t in sub]
        rank_sum = {}
        for p in x:
            try:
                rank_sum[p[1]] = rank_sum[p[1]] + p[0]
            except KeyError:
                rank_sum[p[1]] = p[0]
        print "\nrank_sums", rank_sum

        # Get final scores.
        final_scores = {}
        for a,b in rank_sum.items():
            final_scores[a] = b + raw_scores[a]

        print "final scores", final_scores
        
class AwardsList(ListView):
    template_name = 'awards-list.html'
    model = Award
    context_object_name = 'awards'

    def get_context_data(self, **kwargs):
        context = super(AwardsList, self).get_context_data(**kwargs)
        awards = context['awards']
        totals = []
        counts = []
        statuses = []
        for award in awards:
            total = Award.objects.filter(code=award.code,
                projects__isnull=False).count() * 3
            count = JudgingResult.objects.filter(award=award.code).count()
            totals.append(total)
            counts.append(count)
            if total == count and count is not 0:
                status = True
                #self.get_award_winner(JudgingResult.objects.filter(award=award))
            else:
                status = False
            statuses.append(status)
        context['awards'] = zip(awards, totals, counts, statuses)
        
        return context
    
