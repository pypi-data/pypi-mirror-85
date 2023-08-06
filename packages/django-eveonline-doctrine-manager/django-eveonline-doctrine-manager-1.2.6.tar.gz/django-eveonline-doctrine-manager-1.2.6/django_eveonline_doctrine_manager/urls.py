from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from django_eveonline_doctrine_manager.views import api, doctrines, fittings, skillplans, seeding

urlpatterns = []

urlpatterns += [
    path('api/report/generate', api.generate_character_report, 
        name="django-eveonline-doctrine-manager-api-generate-character-report"),
    path('api/report/doctrines', api.get_character_report,
         name='django-eveonline-doctrine-manager-api-report-doctrines'),
    path('api/doctrines', api.get_character_doctrines,
         name='django-eveonline-doctrine-manager-api-get-doctrines'),
    path('api/fittings', api.get_character_fittings,
         name='django-eveonline-doctrine-manager-api-get-fittings'),
    path('api/skillcheck', api.skillcheck_utility, 
        name='django-eveonline-doctrine-manager-api-skillcheck'),
    path('api/hangarcheck', api.hangarcheck_utility, 
         name='django-eveonline-doctrine-manager-api-hangarcheck'),
    path('api/fitting', api.get_fitting, 
         name='django-eveonline-doctrine-manager-api-get-fitting'),
]

# Doctrines
urlpatterns += [
    path('doctrines/create/',  
        permission_required('django_eveonline_doctrine_manager.add_evedoctrine', raise_exception=True)
        (doctrines.DoctrineCreateView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-create"),

    path('doctrines/', 
         permission_required('django_eveonline_doctrine_manager.view_evedoctrine', raise_exception=True)
        (doctrines.DoctrineListView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-list"),

    path('doctrines/view/<int:id>/', 
         permission_required(
             'django_eveonline_doctrine_manager.view_evedoctrine', raise_exception=True)
        (doctrines.DoctrineDetailView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-detail"),

    path('doctrines/view/<int:id>/audit/', 
         permission_required(
             'django_eveonline_doctrine_manager.view_evecharacterdoctrinereport', raise_exception=True)
        (doctrines.DoctrineAuditView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-audit"),

    path('doctrines/update/<int:id>/', 
         permission_required(
             'django_eveonline_doctrine_manager.change_evedoctrine', raise_exception=True)
        (doctrines.DoctrineUpdateView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-update"),

    path('doctrines/delete/<int:id>/', 
         permission_required(
             'django_eveonline_doctrine_manager.delete_evedoctrine', raise_exception=True)
        (doctrines.DoctrineDeleteView.as_view()),
        name="django-eveonline-doctrine-manager-doctrines-delete"),
]

# Fittings
urlpatterns += [
    path('fittings/create', 
        permission_required('django_eveonline_doctrine_manager.add_evefitting', raise_exception=True)
        (fittings.FittingCreateView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-create"),

    path('fittings', 
        permission_required('django_eveonline_doctrine_manager.view_evefitting', raise_exception=True)
        (fittings.FittingListView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-list"),

    path('fittings/view/<int:id>', 
        permission_required('django_eveonline_doctrine_manager.view_evefitting', raise_exception=True)
        (fittings.FittingDetailView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-detail"),

    path('fittings/view/<int:id>/audit/', 
        permission_required('django_eveonline_doctrine_manager.view_evecharacterdoctrinereport', raise_exception=True)
        (fittings.FittingAuditView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-audit"),

    path('fittings/update/<int:id>', 
        permission_required('django_eveonline_doctrine_manager.change_evefitting', raise_exception=True)
        (fittings.FittingUpdateView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-update"),

    path('fittings/delete/<int:id>', 
        permission_required('django_eveonline_doctrine_manager.delete_evefitting', raise_exception=True)
        (fittings.FittingDeleteView.as_view()),
        name="django-eveonline-doctrine-manager-fittings-delete"),
    
    path('fittings/market/',
         permission_required(
             'django_eveonline_doctrine_manager.view_evefittingmarketrule', raise_exception=True)
         (seeding.FittingMarketRuleListView.as_view()),
         name="django-eveonline-doctrine-manager-fittings-market"),

    path('fittings/market/stock/',
         permission_required(
             'django_eveonline_doctrine_manager.view_evefittingmarketrule', raise_exception=True)
         (seeding.update_stock),
         name="django-eveonline-doctrine-manager-fittings-stock"),
]

# Skillplans
urlpatterns += [
    path('skillplans/create', 
        permission_required(
            'django_eveonline_doctrine_manager.add_eveskillplan', raise_exception=True)
        (skillplans.SkillPlanCreateView.as_view()),
        name="django-eveonline-doctrine-manager-skillplans-create"),

    path('skillplans', 
        permission_required(
            'django_eveonline_doctrine_manager.view_eveskillplan', raise_exception=True)
        (skillplans.SkillPlanListView.as_view()),
        name="django-eveonline-doctrine-manager-skillplans-list"),

    path('skillplans/view/<int:id>', 
        permission_required(
            'django_eveonline_doctrine_manager.view_eveskillplan', raise_exception=True)
        (skillplans.SkillPlanDetailView.as_view()),
        name="django-eveonline-doctrine-manager-skillplans-detail"),

    path('skillplans/update/<int:id>', 
        permission_required(
            'django_eveonline_doctrine_manager.change_eveskillplan', raise_exception=True)
        (skillplans.SkillPlanUpdateView.as_view()),
        name="django-eveonline-doctrine-manager-skillplans-update"),

    path('skillplans/delete/<int:id>', 
        permission_required(
            'django_eveonline_doctrine_manager.change_eveskillplan', raise_exception=True)
        (skillplans.SkillPlanDeleteView.as_view()),
        name="django-eveonline-doctrine-manager-skillplans-delete"),
]

# SRP
urlpatterns += [

]
