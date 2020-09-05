from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import ExpressionWrapper, F, Func, Q, Sum
from django.db.models.functions import Coalesce, Round, ExtractYear, ExtractWeek


class Department(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    date_modified = models.DateTimeField(default=timezone.now, blank=True)
    #created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='casetype_created_by')
    #modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,  related_name='casetype_modified_by')

    def __str__(self):
        return self.name


class CaseType(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=1)
    minutes = models.FloatField()
    description = models.CharField(max_length=250, blank=True, null=True, help_text='Optional. Description of the task (Eg. Used for when case handlers log PPI cases, etc)')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='casetype_created_by')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,  related_name='casetype_modified_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'case type'
        verbose_name_plural = 'case types'
        ordering = ['name']


class CaseQuerySet(models.QuerySet):

    def get_week(self):
            return self.filter(date__week=36)

    def total(self):
        return round(self.select_related('case_type').aggregate(total=Coalesce(Sum('case_type__minutes'),0))['total'],1)

    def total_pct(self):
        return round(self.total() / 450 * 100, 1)
        

class Case(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_case')
    date = models.DateField(default=timezone.now, help_text="Date the case handler worked and claimed for the case. Shown as the 'date added' field on the case log.")
    case_type = models.ForeignKey(CaseType, on_delete=models.CASCADE, verbose_name='Case Type')
    case_ref = models.CharField('CET Reference', max_length=12)
    note = models.CharField('Notes', max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True) # help_text="Date the case was originally added to case log.")
    date_modified = models.DateTimeField(auto_now=True) # help_text="Date will be differ to 'date created' if the case date, type or reference has been modified since insertion.")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='created_by_user')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='modified_by_user')

    objects = CaseQuerySet.as_manager()

    class Meta:
        verbose_name = 'case'
        verbose_name_plural = 'case manager'
        # constraints = [
        #     models.UniqueConstraint(fields=["user", "date", "cet_ref"], name="unique_ref_date")
        # ]

    def __str__(self):
        return self.user.username

    