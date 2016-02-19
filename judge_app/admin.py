from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import (
    ForeignKeyWidget,
    ManyToManyWidget,
    IntegerWidget,
)
from .models import (
    Student,
    Project,
    Award,
    JudgingResult,
)


class StudentResource(resources.ModelResource):
    project = fields.Field(column_name='Project ID',
        attribute='project',
        widget=ForeignKeyWidget(Project, 'project_id'))
    first_name = fields.Field(column_name="Fname",
        attribute='first_name') 
    last_name = fields.Field(column_name="Lname",
        attribute='last_name')
    response_id = fields.Field(column_name="ResponseID",
        attribute='response_id')
    school = fields.Field(column_name="School",
        attribute='school')
    phone = fields.Field(column_name="Contact Phone",
        attribute='phone')
    gender = fields.Field(column_name="Gender",
        attribute='gender')
    grade_level = fields.Field(column_name="Grade Level",
        attribute='grade_level')
    
    class Meta:
        model = Student
        skip_unchanged = False
        import_id_fields = ('response_id',)
        #fields = ('response_id', 'Fname', 'project')


class ProjectResource(resources.ModelResource):
    project_id = fields.Field(column_name="Project ID",
        attribute='project_id')
    title = fields.Field(column_name="Project Title",
        attribute='title')
    awards = fields.Field(column_name="All Award Codes",
        attribute='awards',
        widget=ManyToManyWidget(Award, field='code', separator=';'))

    class Meta:
        model = Project
        skip_unchanged = False
        import_id_fields = ('project_id',)
        fields = ('project_id','title', 'awards',)
    

class AwardResource(resources.ModelResource):
    category = fields.Field(column_name="Category",
        attribute='category')
    code = fields.Field(column_name="Category Code",
        attribute='code')
    number_of_winners = fields.Field(column_name="Number of Winners",
        attribute='number_of_winners',
        default=3,
        widget=IntegerWidget())
    number_of_judges = fields.Field(column_name="Number of Judges",
        attribute='number_of_judges',
        default=3,
        widget=IntegerWidget())
     
    class Meta:
        model = Award
        skip_unchanged = False
        import_id_fields = ('code',)
        fields = ('code','category','number_of_winners', 'number_of_judges',)


class ProjectInline(admin.TabularInline):
    model = Award.projects.through
    extra = 1


class StudentInline(admin.StackedInline):
    model = Student
    extra = 1


class WinnerInline(admin.TabularInline):
    model = Award.winners.through
    extra = 1


class AwardInline(admin.TabularInline):
    model = Project.awards.through
    extra = 1


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_filter = ['project',]


class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    #readonly_fields = ('final_score',)
    inlines = (StudentInline, AwardInline, WinnerInline,)


class AwardAdmin(ImportExportModelAdmin):
    resource_class = AwardResource
    model = Award
    inlines = (ProjectInline,)
    readonly_fields = ('projects', 'winners',)


class JudgeResultAdmin(admin.ModelAdmin):
    model = JudgingResult
    list_filter = ('judge_id', 'project', 'award',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(JudgingResult, JudgeResultAdmin)

