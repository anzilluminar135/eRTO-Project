from django import template

from . import models


register = template.Library()

@register.simple_tag
def get_service_name(obj):

    service = None

    status = obj.application_status

    if isinstance(obj,models.Vehicles):

        service ='New Vehicle Registration'

    elif isinstance(obj,models.RegistrationRenewal):

        service = 'Registration Renewal'

    elif isinstance(obj,models.LearnersLicence):

        service = 'Learners Licence' 

    elif isinstance(obj,models.DrivingLicence):

        service = 'Driving Licence'

    elif isinstance(obj,models.NationalPermit):

        service = 'National Permit'

    elif isinstance(obj,models.TransferOfOwnership):

        service = 'Transfer of Ownership'

    return {'service':service,'status':status}           


@register.simple_tag
def check_user_authenticated(request):

    user = None

    if request.user.is_authenticated:

        user = request.user

    return user    