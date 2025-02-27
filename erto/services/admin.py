from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Vehicles)

admin.site.register(models.RegistrationRenewal)

admin.site.register(models.TransferOfOwnership)

admin.site.register(models.LearnersLicence)

admin.site.register(models.DrivingLicence)

admin.site.register(models.NationalPermit)

admin.site.register(models.Payments)

admin.site.register(models.Transactions)

