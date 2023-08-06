from django.contrib import admin
from django import forms
from .models import *
from django_singleton_admin.admin import DjangoSingletonModelAdmin

admin.site.register(EveDoctrineSettings, DjangoSingletonModelAdmin)
admin.site.register(EveDoctrineRole)
admin.site.register(EveDoctrineManagerTag)
admin.site.register(EveDoctrineCategory)
admin.site.register(EveFittingMarketRule)
