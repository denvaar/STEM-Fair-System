from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import Student, Project


# Register your models here.

class StudentResource(resources.ModelResource):
    project = fields.Field(column_name='Project Title',
        attribute='project',
        widget=ForeignKeyWidget(Project, 'title'))
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
        skip_unchanged = True
        import_id_fields = ('response_id',)
        #fields = ('response_id', 'Fname', 'project')

class ProjectResource(resources.ModelResource):
    project_id = fields.Field(column_name="Project ID",
        attribute='project_id')
    title = fields.Field(column_name="Project Title",
        attribute='title')
    award_code = fields.Field(column_name="Award Code",
        attribute='award_code')
    class Meta:
        model = Project
        skip_unchanged = True
        import_id_fields = ('project_id',)
        fields = ('project_id','title', 'award_code')

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    pass

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_filter = ['award_code',]

admin.site.register(Student, StudentAdmin)
admin.site.register(Project, ProjectAdmin)

