
import csv
from datetime import datetime, timedelta

from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from .forms import TriageCaseCreate, CaseUpdate, TmTriageCaseCreate, CaseTypeForm, ExportForm, CalcCaseCreate
from .models import Case, CaseType
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Max, Min, Sum, ExpressionWrapper, F, Func
from django.db.models import ExpressionWrapper, F, Func, Q, Sum, OuterRef, Subquery
from django.db.models.functions import Coalesce, Round, ExtractYear, ExtractWeek

User = get_user_model()




@login_required
def ch_case_list_view(request):

    user_ = request.user
    today = timezone.now()
    week_number = timezone.now().isocalendar()[1]
    cases = Case.objects.filter(user=user_, date=today).order_by('-date', '-date_modified')
    weektotal = Case.objects.filter(user=user_, date__week=week_number).order_by('-date', '-date_modified')

    if str(request.user.department) == 'Triage':
        if request.method == 'POST':
            form = TriageCaseCreate(request.POST, user=user_, date=today)
            if form.is_valid():
                form.instance.user = user_
                form.save()
                messages.success(request, f'{form.instance.case_ref} - {form.instance.case_type} has been added')
                return redirect('prod:list')
        else:
            form = TriageCaseCreate(user=user_, date=today)
    else:
        if request.method == 'POST':
            form = CalcCaseCreate(request.POST, user=user_, date=today)
            if form.is_valid():
                form.instance.user = user_
                form.save()
                messages.success(request, f'{form.instance.case_ref} - {form.instance.case_type} has been added')
                return redirect('prod:list')
        else:
            form = CalcCaseCreate(user=user_, date=today)
    

    context = {
        'week_number': week_number,
        'user': user_,
        'weektotal': weektotal,
        'object_list': cases,
        'form': form,
        'today': today,
    }
    return render(request, 'productivity/case_list.html', context)



@login_required
def case_create_view(request):

    if request.method == 'POST':
        form = CaseUpdate(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, f'Case added')
            return redirect('prod:list')
    else:
        form = CaseUpdate()

    context = {
        'title': 'Update Case',
        'form': form,
    }
    return render(request, 'productivity/case_form.html', context)



@login_required
def case_delete_view(request, pk=None):
    obj = get_object_or_404(Case, id=pk)
    today = timezone.now()
    if request.method == 'POST':
        print(obj.date)
        if obj.date != timezone.now().date():
            messages.error(request, 'ERROR: You are unable delete cases worked prior to today. Please speak to your TM in the first instance. Case not deleted.')
            return redirect('prod:list')
        else:
            obj.delete()
            messages.warning(request, f'{obj.case_ref} - {obj.case_type} has been deleted')
            return redirect('prod:list')

    context = {'object': obj}
    return render(request, 'productivity/case_confirm_delete.html', context)





@login_required
@staff_member_required
def tm_case_delete_view(request, pk=None):
    obj = get_object_or_404(Case, id=pk)

    if request.method == 'POST':
        obj.delete()
        messages.warning(request, f'{obj.case_ref} - {obj.case_type} has been deleted')
        return redirect(f'/tm-view/{obj.user.id}')

    context = {'object': obj}
    return render(request, 'productivity/case_confirm_delete.html', context)




"""
TM Views
Only TMs can update cases that have already been put on caseflow.
"""

@login_required
@staff_member_required
def team_list_view(request):
    today = timezone.now()
    week_number = timezone.now().isocalendar()[1]
    mon = today - timedelta(days=today.weekday())
    tue = mon + timedelta(days=1)
    wed = mon + timedelta(days=2)
    thu = mon + timedelta(days=3)
    fri = mon + timedelta(days=4)
    sat = mon + timedelta(days=5)
    sun = mon + timedelta(days=6)    

    object_list = (
        User.objects.all().order_by('-department')

        # getting date last case worked
        .annotate(
            last_case=Subquery(
                Case.objects.filter(user=OuterRef("pk"),).order_by('-date_created').values(
                    "date_created"
                )[:1]
            )
        )
        # Getting last case ref
        .annotate(
            last_case_ref=Subquery(
                Case.objects.filter(user=OuterRef("pk"),).order_by('-date_created').values(
                    "case_ref"
                )[:1]
            )
        )

        # Getting the total prod for today
        .annotate(
            total_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=today).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            # prod for current week
            .annotate(
            total_week=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date__week=week_number).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            # Monday's prod
            .annotate(
            mon_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=mon).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            # Tue prod
            .annotate(
            tue_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=tue).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            # Tue prod
            .annotate(
            wed_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=wed).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )

            .annotate(
            thu_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=thu).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
                            # Tue prod
            .annotate(
            fri_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=fri).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            .annotate(
            sat_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=sat).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
                
            .annotate(
            sun_prod=Subquery(
                Case.objects.select_related('case_type').filter(user=OuterRef("pk"), date=sun).values_list('user').annotate(
                    case_count=Sum('case_type__minutes')).values('case_count'))
                )
            )            
        
    


    q = request.GET.get("q")
    if q:
        object_list = object_list.filter(
            Q(id__icontains=q)
            | Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
        )  # .distinct()

    paginator = Paginator(object_list, 50)
    page = request.GET.get("page")
    object_list = paginator.get_page(page)

    context = {
        'object_list': object_list
        }
    return render(request, 'productivity/team_list.html', context)



@login_required
@staff_member_required
def tm_case_list_view(request, pk):
    """ View for TMs and OMs to see individual case handlers Prod """

    user_ = get_object_or_404(User, id=pk)
    today = timezone.now()
    week_number = timezone.now().isocalendar()[1]
    cases = Case.objects.filter(user=user_, date=today).order_by('-date', '-date_modified')
    weektotal = Case.objects.filter(user=user_, date__week=week_number).order_by('-date', '-date_modified')

    if request.method == 'POST':
        form = TmTriageCaseCreate(request.POST, user=user_, date=today)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user_

            instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
            return redirect(f'/tm-view/{pk}')
    else:
        form = TmTriageCaseCreate(user=user_, date=today)

    context = {
        'week_number': week_number,
        'user': user_,
        'weektotal': weektotal,
        'object_list': cases,
        'form': form,
        'today': today,
    }
    return render(request, 'productivity/case_list_tm.html', context)



@login_required
@staff_member_required
def case_update_view(request, pk=None):
    obj = get_object_or_404(Case, id=pk)

    if request.method == 'POST':
        form = CaseUpdate(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updated_by = request.user
            instance.save()
            messages.warning(request, f'{obj.case_ref} - {obj.case_type} for {obj.user} has been updated')
            return redirect(f'/tm-view/{obj.user.id}')
    else:
        form = CaseUpdate(instance=obj)

    context = {
        'title': 'Update Case',
        'form': form,
    }
    return render(request, 'productivity/case_form.html', context)


@login_required
@staff_member_required
def csv_export(request):

    response = HttpResponse(content_type='text/csv')   
    writer = csv.writer(response)
    writer.writerow(['user', 'date_claimed', 'department', 'case_type', 'case_ref', 'note', 'date_added', 'date_modified'])
    for x in Case.objects.all().values_list('user__username', 'date', 'case_type__department__name', 'case_type__name', 'case_ref', 'note', 'date_created', 'date_modified'):
        writer.writerow(x)
    response['Content-Disposition'] = 'attachment; filename="case-report.csv"'
    return response


@login_required
@staff_member_required
def csv_case_type_export(request):
    response = HttpResponse(content_type='text/csv')   
    writer = csv.writer(response)
    writer.writerow(['case_type_name', 'minute_value', 'date_created', 'date_modified'])
    for x in CaseType.objects.all().values_list('name', 'minutes', 'date_created', 'date_modified'):
        writer.writerow(x)  
    response['Content-Disposition'] = 'attachment; filename="case-report.csv"'
    return response




@login_required
@staff_member_required
def site_map_view(request):
    """ TEMP View to show every feature/page of the site """
    context = {
    }
    return render(request, 'sitemap.html', context)










@login_required
@staff_member_required
def full_case_list_view(request):

### CHANGED TO USE SELECT RELATED!!!
    object_list = Case.objects.all().select_related('case_type').order_by('-date', '-date_modified')
    q = request.GET.get("q")
    if q:
        object_list = object_list.filter(
            Q(date__icontains=q)
            | Q(user__username__icontains=q)
            | Q(case_type__department__name__icontains=q)
            | Q(case_type__name__icontains=q)
            | Q(case_ref__icontains=q)
        )  # .distinct()

    # total case count
    total_idv_count = object_list.filter(case_type__name='IDV Proof').aggregate(casecount=Count('case_type__name'))['casecount']
    total_ff_count = object_list.filter(case_type__name='Final Final').aggregate(casecount=Count('case_type__name'))['casecount']
    total_ffs_count = object_list.filter(case_type__name='Final Final Shell').aggregate(casecount=Count('case_type__name'))['casecount']
    total_reclass_count = object_list.filter(case_type__name='Reclassified').aggregate(casecount=Count('case_type__name'))['casecount']
    total_count = object_list.aggregate(casecount=Count('case_type__name'))['casecount']

    # total mins sum
    total_idv_mins = object_list.filter(case_type__name='IDV Proof').aggregate(mins=Sum('case_type__minutes'))['mins']
    total_ff_mins = object_list.filter(case_type__name='Final Final').aggregate(mins=Sum('case_type__minutes'))['mins']
    total_ffs_mins = object_list.filter(case_type__name='Final Final Shell').aggregate(mins=Sum('case_type__minutes'))['mins']
    total_reclass_mins = object_list.filter(case_type__name='Reclassified').aggregate(mins=Sum('case_type__minutes'))['mins']
    total_mins = object_list.aggregate(mins=Sum('case_type__minutes'))['mins']
    # Search query - can search by the below parameters


    paginator = Paginator(object_list, 38)
    page = request.GET.get("page")
    object_list = paginator.get_page(page)


    context = {
        'total_idv_count': total_idv_count,
        'total_ff_count': total_ff_count,
        'total_ffs_count': total_ffs_count,
        'total_reclass_count': total_reclass_count,
        'total_count': total_count,

        'total_idv_mins': total_idv_mins,
        'total_ff_mins': total_ff_mins,
        'total_ffs_mins': total_ffs_mins,
        'total_reclass_mins': total_reclass_mins,
        'total_mins': total_mins,
        'object_list': object_list,
    }
    return render(request, 'productivity/full_case_list.html', context)



@login_required
@staff_member_required
def operational_stats_view(request):
    
    user_list = User.objects.all()
    fs_day = []
    mins_day = []
    for user in user_list:
        fs_day.append(user.username)
        mins_day.append(User.query.filter(id=user.id).total_mins_today())
    today_total = dict(zip(fs_day, mins_day))

    fs_week = []
    mins_week = []
    for user in user_list:
        fs_week.append(user.username)
        mins_week.append(User.query.filter(id=user.id).total_mins_week())
    week_total = dict(zip(fs_week, mins_week))

    context = {
        'user_list': user_list,
        'day': today_total, 
        'week': week_total
    }

    return render(request, 'productivity/full_ch_stats.html', context)










    """ CASE TYPE VIEWS """


def casetype_list_view(request):
    object_list = CaseType.objects.all().order_by('-department')

    # Search functionality
    q = request.GET.get("q")
    if q:
        object_list = object_list.filter(
            Q(name__icontains=q)
            | Q(department__name__icontains=q)
            | Q(minutes__icontains=q)
            | Q(description__icontains=q)
        )  # .distinct()

    paginator = Paginator(object_list, 100)
    page = request.GET.get("page")
    object_list = paginator.get_page(page)

    context = {
        'object_list': object_list,
    }
    return render(request, 'productivity/casetype_list.html', context)


def casetype_create_view(request):
    if request.method == 'POST':
        form = CaseTypeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            messages.success(request, f'New task {instance.name} has been created')
            return redirect('prod:casetype_list')
    else:
        form = CaseTypeForm()
    context = {
        'title': 'Create New Task',
        'form': form,
    }
    return render(request, 'productivity/casetype_form.html', context)


def casetype_detail_view(request, pk):
    obj = get_object_or_404(CaseType, id=pk)
    context = {
        'object': obj,
    }
    return render(request, 'productivity/casetype_detail.html', context)


def casetype_update_view(request, pk):
    obj = get_object_or_404(CaseType, id=pk)
    if request.method == 'POST':
        form = CaseTypeForm(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.save()
            messages.success(request, f'Task - {instance.name} has been updated')
            return redirect(f'prod:casetype_list')
    else:
        form = CaseTypeForm(instance=obj)
    context = {
        'title': 'Update Task',
        'form': form,
    }
    return render(request, 'productivity/casetype_form.html', context)



def casetype_delete_view(request, pk):
    obj = get_object_or_404(CaseType, id=pk)
    if request.method == 'POST':
        obj.delete()
        messages.warning(request, f'{obj.name} for {obj.minutes} minutes has been deleted')
        return redirect('prod:casetype_list')
    context = {
        'object': obj,
    }
    return render(request, 'productivity/casetype_confirm_delete.html', context)




        
# in prog
def export_list_view(request):
    form = ExportForm(request.POST or None)
    download_form = None

    if request.method =='POST':
        
        if form.is_valid():
            pass
    context ={
        'form': form,
        'download_form': download_form,
    }
    return render(request, 'productivity/reports.html', context)


