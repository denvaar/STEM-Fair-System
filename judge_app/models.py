from __future__ import unicode_literals

from django.db import models


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
    code = models.CharField(primary_key=True, max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    grade_range = models.CharField(max_length=10,
        blank=True, null=True)
    projects = models.ManyToManyField('Project',
        related_name='awards',
        blank=True)
    
    def save(self):
        if not self.grade_range:
            try:
                self.grade_range = self.code.split()[1]
            except KeyError:
                pass
        if not self.title:
            self.title = "{0} {1}".format(self.grade_range, self.category)
        super(Award, self).save()

    def __unicode__(self):
        return "{0}".format(self.code)


class JudgingResult(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    award = models.ForeignKey('Award', on_delete=models.CASCADE)
    judge_id = models.CharField(max_length=255, help_text="Judge ID")
    score = models.IntegerField(help_text="Score")

    def __unicode__(self):
        return "Project: {2} Score: {0} Award: {1}".format(\
            self.score, self.award, self.project)


class Project(models.Model):
    project_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=250)
    # Related fields:
    # judgingresult_set
    # student_set 

    def __unicode__(self):
        return self.project_id

