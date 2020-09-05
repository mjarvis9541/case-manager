import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()


def staff_view(request):
    object_list = User.objects.all()

    context = {
        'object_list': object_list,
    }
    return render(request, 'accounts/user_list.html', context)




def login_view(request):
    if request.user.is_authenticated:
        return redirect('prod:list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('prod:list')
            else:
                messages.warning(request, 'Incorrect username/password.')
                return redirect('/')          
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:logout')
    return render(request, 'accounts/logout.html')




@login_required
@staff_member_required
def csv_export(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'])
    for x in User.objects.all().values_list('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'):
        writer.writerow(x)
    
    response['Content-Disposition'] = 'attachment; filename="user-report.csv"'
    return response