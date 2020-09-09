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

    path('user/', views.UserListView.as_view(), name='user_list'),
    path('user/new/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]

