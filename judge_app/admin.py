from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from .models import Student, Project


# Register your models here.

class StudentResource(resources.ModelResource):
    project = fields.Field(column_name='project',
        attribute='project',
        widget=ForeignKeyWidget(Project, 'title'))
    
    class Meta:
        model = Student
        skip_unchanged = True
        fields = ('id', 'name', 'project')

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        skip_unchanged = True
        fields = ('id','title')

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    pass

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    pass

admin.site.register(Student, StudentAdmin)
admin.site.register(Project, ProjectAdmin)

