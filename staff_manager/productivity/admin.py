from django.contrib import admin
from .models import Case, CaseType, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Department._meta.fields if f.name != 'id']
    #readonly_fields = ['date_created', 'date_modified']

class CaseAdmin(admin.ModelAdmin):
    list_display = [
        'case_ref',
        'case_type',
        'date',
        'user',
        'note',
        'date_created',
        'date_modified',
    ]
    readonly_fields = ['date_created', 'date_modified']


class CaseTypeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CaseType._meta.fields if f.name != 'id']
    # list_filter = ['name', 'prod']
    # search_fields = ['name']
    readonly_fields = ['date_created', 'date_modified']

# Register your models here.
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseType, CaseTypeAdmin)
admin.site.register(Department, DepartmentAdmin)