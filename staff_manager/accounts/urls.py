from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('staff/', views.staff_view),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Reports - exporting data to CSV
    path('export', views.csv_export, name='export'),

    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),


]

