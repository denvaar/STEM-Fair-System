import operator
from collections import defaultdict
from itertools import groupby

from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .mixins import PDFTemplateResponseMixin
from .forms import ScoreForm
from .models import (
    Award,
    Project,
    JudgingResult,
    AwardWinner,
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
    success_url = reverse_lazy('score-submit')

    def get_context_data(self, **kwargs):
        context = super(ScoreSubmissionView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Called when the valid form data has been POSTed.
        fv = super(ScoreSubmissionView, self).form_valid(form)
        award_id = form.data['award']
        award = Award.objects.get(code=award_id)
        total_judges = len(award.projects.all()) * award.number_of_judges
        submissions = JudgingResult.objects.filter(award=award).count()
        if submissions == total_judges:
            if self.check_unique_ids(award_id) and \
            self.check_projects(award, total_judges):
                self.get_award_results(award_id)
                messages.success(self.request,
                    "Thank you! Score recorded successfully. Award complete!")
        else:
            messages.success(self.request,
                "Thank you! Score recorded successfully.")
        return fv

    def form_invalid(self, form):
        return super(ScoreSubmissionView, self).form_invalid(form)

    def check_projects(self, award, total_scores):
        results = JudgingResult.objects.filter(award=award)
        try:
            if len(results.distinct('project', 'judge_id')) == \
                total_scores:
                return True
        except NotImplementedError:
            if len(results.values('project', 'judge_id').distinct()) == \
                total_scores:
                return True
        messages.error(self.request,
            "Projects not judged evenly. Check the admin setup.")
        return False
            

    def check_unique_ids(self, award_id):
        try:
            if len(JudgingResult.objects.distinct('judge_id'))\
                != Award.objects.get(code=award_id).number_of_judges:
                messages.error(self.request,
                    "Incorrect number of unique judges. Check the admin setup.")
                return False
        except NotImplementedError:
            if len(JudgingResult.objects.values('judge_id').distinct())\
                != Award.objects.get(code=award_id).number_of_judges:
                messages.error(self.request,
                    "Incorrect number of unique judges. Check the admin setup.")
                return False
        return True

    def get_award_results(self, award_id):
        award = Award.objects.get(code=award_id)
        judges = award.number_of_judges

        total = Award.objects.filter(code=award_id,
            projects__isnull=False).count() * award.number_of_judges
        
        results = JudgingResult.objects.filter(award=award_id)
       
        if results.count() < total:
            # Not time to compute winners yet.
            return
        raw_scores = {}
        judge_scores = {}
        for r in results.all():
            try:
                judge_scores[r.judge_id].append(\
                    (r.project.project_id,r.score))
            except KeyError:
                judge_scores[r.judge_id] = \
                    [(r.project.project_id,r.score)]
            try:
                raw_scores[r.project.project_id] = \
                    raw_scores[r.project.project_id] + r.score
            except KeyError:
                raw_scores[r.project.project_id] = r.score
        raw_scores = dict(\
            [(k,v/(judges * 100.0))
            for k,v in raw_scores.iteritems()]
        )
        print raw_scores
        print judge_scores
        # sort each judge's scores for each project
        for j in judge_scores.items():
            for p in j[1]:
                j[1].sort(key=operator.itemgetter(1),
                    reverse=True)
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
        award = Award.objects.get(code=award_id)
        winners = sorted(
            final_scores.items(),
            key=operator.itemgetter(1)
        )[:award.number_of_winners]
        print winners
        for i in range(0, len(winners[:award.number_of_winners])):
            p = Project.objects.get(project_id=winners[i][0])
            winner = AwardWinner(
                project=p,
                award=award,
                final_score=round(winners[i][1], 5)
            )
            winner.save()

class AwardsDetail(DetailView):
    template_name = 'awards-detail.html'
    model = Award
    context_object_name = 'award'

    def get_context_data(self, **kwargs):
        context = super(AwardsDetail, self).get_context_data(**kwargs)
        winners = AwardWinner.objects.filter(\
            award=context['award']).order_by('final_score')

        context['winners'] = AwardWinner.objects.filter(\
            award=context['award']).order_by('final_score')
        return context

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
                projects__isnull=False).count() * award.number_of_judges
            count = JudgingResult.objects.filter(award=award.code).count()
            totals.append(total)
            counts.append(count)
            if total == count and count is not 0:
                if AwardWinner.objects.filter(award=award):
                    status = True
                else:
                    status = False
                #self.get_award_winner(JudgingResult.objects.filter(award=award))
            else:
                status = False
            statuses.append(status)
        context['awards'] = zip(awards, totals, counts, statuses)
        
        return context
    
class PresentationList(ListView):
    template_name = 'presentation-list.html'
    context_object_name = 'awards'
    paginate_by = 1
    
    def get_queryset(self):
        queryset = Award.objects.exclude(awardwinner=None).order_by('presentation_order')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PresentationList, self).get_context_data(**kwargs)
        #for i,award_obj in enumerate(context['awards']):
        #    context['awards'][i].awardwinner_set.order_by('final_score')
        return context

class WinnersPDFView(PDFTemplateResponseMixin, ListView):
    template_name = 'presentation-list.html'
    context_object_name = 'awards'
    pdf_filename = 'results.pdf'
    
    def get_queryset(self):
        queryset = Award.objects.exclude(awardwinner=None)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WinnersPDFView, self).get_context_data(**kwargs)
        # check for ties.
        return context
    
