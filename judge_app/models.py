from __future__ import unicode_literals

from django.db import models

from autoslug import AutoSlugField

class Student(models.Model):
    response_id = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.first_name + " " + self.last_name
    

class Award(models.Model):
    slug = AutoSlugField(populate_from='code', unique=True)
    code = models.CharField(primary_key=True, max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    grade_range = models.CharField(max_length=10,
        blank=True, null=True)
    projects = models.ManyToManyField('Project',
        related_name='awards',
        blank=True)
    winners = models.ManyToManyField('Project',
        related_name='winners',
        through='AwardWinner',
        blank=True)
    number_of_winners = models.IntegerField(default=3)
    number_of_judges = models.IntegerField(default=3)
    
    def save(self):
        if not self.grade_range:
            try:
                self.grade_range = self.code.split()[1]
                if not self.title:
                    self.title = "{0} {1}".format(self.grade_range, self.category)
            except (KeyError, IndexError):
                self.title = self.category
                self.category = "Specialty Award"
        super(Award, self).save()

    def __unicode__(self):
        return "{0}".format(self.code)


class JudgingResult(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    award = models.ForeignKey('Award', on_delete=models.CASCADE,
        help_text="The awards that this judge will be judging.")
    #judge_id = models.CharField(max_length=255, help_text="Judge ID")
    judge_id = models.ForeignKey('Judge', on_delete=models.CASCADE)
    score = models.IntegerField(help_text="Score")

    def __unicode__(self):
        return "Project: {2} Score: {0} Award: {1}".format(\
            self.score, self.award, self.project)

class Judge(models.Model):
    judge_id = models.CharField(max_length=255, primary_key=True)
    awards = models.ManyToManyField('Award', blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "{0}".format(self.judge_id)

class AwardWinner(models.Model):
    award = models.ForeignKey('Award', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    final_score = models.DecimalField(max_digits=15,
        decimal_places=7,
        blank=True, null=True)
    

class Project(models.Model):
    project_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=250)

    def __unicode__(self):
        return self.project_id


