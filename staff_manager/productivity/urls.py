from django.urls import path

from . import views

app_name = 'prod'
urlpatterns = [
    
    path('', views.ch_case_list_view, name='list'), # main site view - case log - case handler view
    # path('create/', views.case_create_view, name='create'), # unused - case handlers add prod on the case list page
    path('delete-case/<int:pk>/', views.case_delete_view, name='delete'), # case handlers can delete cases worked today


    # Team leader levels views
    path('teamlist/', views.team_list_view, name='teamlist'), # tm to view list of staff
    path('tm-view/<int:pk>/', views.tm_case_list_view, name='tmview'), # tm access to ch list view

    path('tm-update-case/<int:pk>/', views.case_update_view, name='update'), # a tm view for updating a logged case
    path('tm-delete-case/<int:pk>/', views.tm_case_delete_view, name='tmdelete'), # tms can delete cases prior to today


    # Operation level views
    path('operational-view/', views.full_case_list_view, name='full-case-list'), # view for ops to see production over departments
    path('stats/', views.operational_stats_view, name='ch_stats'), # potential to improve this

    # Reports - exporting data to CSV
    path('export/', views.csv_export, name='export'),
    path('case-type-export/', views.csv_case_type_export, name='case_type_export'),


    # Development site map for links to all areas of the site
    path('sitemap/', views.site_map_view, name='sitemap'),

    
    # CaseType views - list, create, detail, update, delete - complete.
    path('case-type-list/', views.casetype_list_view, name='casetype_list'),
    path('case-type-create/', views.casetype_create_view, name='casetype_create'),
    path('case-type-detail/<int:pk>/', views.casetype_detail_view, name='casetype_detail'),
    path('case-type-update/<int:pk>/', views.casetype_update_view, name='casetype_update'),
    path('case-type-delete/<int:pk>/', views.casetype_delete_view, name='casetype_delete'),

    # Department views - list, create, detail, update, delete - on hold
    # path('department-list/', views.department_list_view, name='department_list'),
    # path('department-create/', views.department_create_view, name='department_create'),
    # path('department-detail/<int:pk>/', views.department_detail_view, name='department_detail'),
    # path('department-update/<int:pk>/', views.department_update_view, name='department_update'),
    # path('department-delete/<int:pk>/', views.department_delete_view, name='department_delete'),

    
    path('reports/', views.export_list_view, name='export_list'),

    # Creating staff memembers

]

