from django.contrib import admin

from apprest.models.experiments import CalipsoExperiment
from apprest.models.facilities import CalipsoFacility
from apprest.models.user import CalipsoUser

admin.site.register(CalipsoFacility)
admin.site.register(CalipsoUser)
admin.site.register(CalipsoExperiment)
