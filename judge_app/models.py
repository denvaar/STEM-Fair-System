from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    response_id = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    # Student has 1 project. A project can have many students.

    def __unicode__(self):
        return self.first_name + " " + self.last_name

class Award(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    grade_range = models.CharField(max_length=10)
    # Possibly use an intermediate model for the winners.
    #winners = models.ManyToMany('Project', on_delete=models.CASCADE)
    judge_count = models.IntegerField(default=1)
    total_evals_per_student = models.IntegerField(default=1)
    remaining_judge_evals = models.IntegerField(default=1)

class Project(models.Model):
    # A project enters 1 award. An award can have many entered projects.
    #registered_award = models.ForeignKey('Award', on_delete=models.CASCADE)
    project_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    score = models.IntegerField(default=0)
    award_code = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title
