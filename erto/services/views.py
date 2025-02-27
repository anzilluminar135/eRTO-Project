from django.shortcuts import render,redirect

from django.views import View

from .forms import RegistrationNumberForm,RegistrationWithChasisForm,VehicleRegistrationForm,RenewalRegistrationForm

from .forms import TransferOfOwnershipForm,LearnersLicenceForm,DrivingLicenceForm,NationalPermitForm,LoginForm,ChasisWithMobForm

from .models import Vehicles,Payments,Transactions,RegistrationRenewal

from .utility import get_vehicle,get_application_number,get_txn_id,get_registration_number,send_email

from django.db import transaction

from django.contrib.contenttypes.models import ContentType

from .models import FeeChoices

from decouple import config

import razorpay

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,login,logout

from itertools import chain

from . import models

from django.db.models import Q

# email related imports

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.conf import settings

import threading

from django.contrib.auth.decorators import login_required




# Create your views here.

# home page view

class HomeView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'services/home.html')
    

        

    

# register number form page view

class RegistrationNumberView(View):

    def get(self,request,*args,**kwargs):

        service = request.GET.get('service')

        request.session['service']=service

        form = RegistrationNumberForm()

        return render(request,'services/register-number.html',context={'form':form,'service':service}) 
    
    def post(self,request,*args,**kwargs):

        form =RegistrationNumberForm(request.POST)

        if form.is_valid():

            registration_number = form.cleaned_data.get('registration_number')

            request.session['registration_number']=registration_number

            return redirect('registration-with-chasis')

        return render(request,'services/register-number.html',context={'form':form})


class RegistrationNumberWithChasisView(View):

    def get(self,request,*args,**kwargs):

        registration_number = request.session['registration_number']

        form = RegistrationWithChasisForm()

        return render(request,'services/register-with-chasis.html',context={'form':form,'registration_number':registration_number})

    def post(self,request,*args,**kwargs):

        form = RegistrationWithChasisForm(request.POST)

        registration_number = request.session['registration_number']

        if form.is_valid():

            # last 5 digits of chasis number

            chasis_last_5_number = form.cleaned_data['chasis_number']

            vehicle = get_vehicle(registration_number,chasis_last_5_number)


            if not vehicle:

                return render(request,'services/register-with-chasis.html',context={'form':form,'registration_number':registration_number,'error':'not find a registered vehicle'})
            
            request.session['chasis_last_5_number'] = chasis_last_5_number

            service = request.session['service']

            if service=='vehicle-registration':

                return redirect('renewal-registration')
            
            elif service == 'transfer-of-ownership':

                return redirect('transfer-ownership')
            
            elif service == 'national-permit':

                return redirect('national-permit')
        
        return render(request,'services/register-with-chasis.html',context={'form':form,'registration_number':registration_number})
    


class RegistrationRenewalView(View):


    def get(self,request,*args,**kwargs):

        chasis_last_5_number = request.session['chasis_last_5_number']

        registration_number = request.session['registration_number']

        vehicle = get_vehicle(registration_number,chasis_last_5_number)


        form = RenewalRegistrationForm(initial={'chasis_number':vehicle.chasis_number,
                                                'engine_number':vehicle.engine_number,
                                                'registration_number':vehicle.registration_number})

        return render(request,'services/renewal-registration.html',context={'form':form})
    
    def post(self,request,*args,**kwargs):

        form = RenewalRegistrationForm(request.POST,request.FILES)


        if form.is_valid():

            with transaction.atomic() : 

                renewal = form.save(commit=False)

                chasis_num =form.cleaned_data['chasis_number']

                registration_number = form.cleaned_data['registration_number']

                vehicle = get_vehicle(chsis_num=chasis_num,reg_num=registration_number)

                renewal.vehicle = vehicle

                renewal.application_number = get_application_number()

                renewal.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(renewal),service_id=renewal.id,fee=FeeChoices.RENEWAL_VEHICLE_REGISTRATION) 

                request.session['service']='vehicle-registration-renewal'

                return render(request,'services/payment-page.html',context={'service':'vehicle-registration-renewal','payment':payment})

        return render(request,'services/renewal-registration.html',context={'form':form})




class VehicleRegistrationView(View):


    def get(self,request,*args,**kwargs):

        form = VehicleRegistrationForm()

        return render(request,'services/vehicle-registration.html',{'form':form})
    
    def post(self,request,*args,**kwargs):

        form = VehicleRegistrationForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                vehicle_reg = form.save(commit=False)

                vehicle_reg.application_number = get_application_number()

                vehicle_reg.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(vehicle_reg),service_id=vehicle_reg.id,fee=FeeChoices.VEHICLE_REGISTRATION_OR_LEARNERS_LICENCE) 

                request.session['service']='new-vehicle-registration'

                return render(request,'services/payment-page.html',context={'service':'new-vehicle-registration','payment':payment})

        return render(request,'services/vehicle-registration.html',{'form':form})
    


class TransferOfOwnershipView(View):


    def get(self,request,*args,**kwargs):

        chasis_last_5_number = request.session['chasis_last_5_number']

        registration_number = request.session['registration_number']

        vehicle = get_vehicle(registration_number,chasis_last_5_number)

        form = TransferOfOwnershipForm()

        return render(request,'services/transfer-of-ownership.html',context={'form':form,'vehicle':vehicle})
    
    def post(self,request,*args,**kwargs):

        form = TransferOfOwnershipForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                transfer_of_ownership = form.save(commit=False)

                chasis_last_5_number = request.session['chasis_last_5_number']

                registration_number = request.session['registration_number']

                vehicle = get_vehicle(registration_number,chasis_last_5_number)

                transfer_of_ownership.vehicle = vehicle

                transfer_of_ownership.application_number = get_application_number()

                transfer_of_ownership.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(transfer_of_ownership),service_id=transfer_of_ownership.id,fee=FeeChoices.TRANSFER_OF_OWNERSHIP) 

                request.session['service']='transfer-of-ownership'

                return render(request,'services/payment-page.html',context={'service':'transfer-of-ownership','payment':payment})

        return render(request,'services/transfer-of-ownership.html',context={'form':form})


# learner's licence application view

class LearnersLicenceView(View):


    def get(self,request,*args,**kwargs):

        form = LearnersLicenceForm()

        return render(request,'services/learners-licence.html',context={'form':form})
    
    def post(self,request,*args,**kwargs):

        form = LearnersLicenceForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                learners_licence = form.save(commit=False)

                learners_licence.application_number = get_application_number()

                learners_licence.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(learners_licence),service_id=learners_licence.id,fee=FeeChoices.VEHICLE_REGISTRATION_OR_LEARNERS_LICENCE) 

                request.session['service']='learners-licence'

                return render(request,'services/payment-page.html',context={'service':'learners-licence','payment':payment})

        return render(request,'services/learners-licence.html',context={'form':form})


# driving licence application view

class DrivingLicenceView(View):


    def get(self,request,*args,**kwargs):

        form = DrivingLicenceForm()

        return render(request,'services/driving-licence.html',context={'form':form})
    
    def post(self,request,*args,**kwargs):

        form = DrivingLicenceForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                driving_licence = form.save(commit=False)

                driving_licence.application_number = get_application_number()

                driving_licence.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(driving_licence),service_id=driving_licence.id,fee=FeeChoices.DRIVING_LICENCE) 

                request.session['service']='driving-licence'

                return render(request,'services/payment-page.html',context={'service':'driving-licence','payment':payment})


        return render(request,'services/driving-licence.html',context={'form':form})
    

class NationalPermitView(View):

    def get(self,request,*args,**kwargs):

        chasis_last_5_number = request.session['chasis_last_5_number']

        registration_number = request.session['registration_number']

        vehicle = get_vehicle(registration_number,chasis_last_5_number)

        form = NationalPermitForm()

        return render(request,'services/national-permit.html',context={'vehicle':vehicle,'form':form}) 
    

    def post(self,request,*args,**kwargs):

        chasis_last_5_number = request.session['chasis_last_5_number']

        registration_number = request.session['registration_number']

        vehicle = get_vehicle(registration_number,chasis_last_5_number)

        form = NationalPermitForm(request.POST,request.FILES)



        if form.is_valid():

            with transaction.atomic():

                national_permit = form.save(commit=False)

                national_permit.vehicle = vehicle

                national_permit.application_number = get_application_number()

                national_permit.save()

                txn_id = get_txn_id()

                payment=Payments.objects.create(txn_id=txn_id,service_type=ContentType.objects.get_for_model(national_permit),service_id=national_permit.id,fee=FeeChoices.NATIONAL_PERMIT) 

                request.session['service']='national-permit'

                return render(request,'services/payment-page.html',context={'service':'national-permit','payment':payment})

        return render(request,'services/national-permit.html',context={'vehicle':vehicle,'form':form}) 
    


class PaymentView(View):

    def post(self,request,*args,**kwargs):

        with transaction.atomic():
  

            fee = int(request.POST.get('fee'))

            payment_uuid = request.POST.get('payment_uuid')
            

            payment_obj = Payments.objects.get(uuid=payment_uuid)

            # authenticating razorpay client

            client = razorpay.Client(auth=(config('RZP_KEY_ID'),config('RZP_KEY_SECRET')))

            # creating order in razorpay

            data = {'amount':fee*100,'currency':'INR', 'receipt': 'receipt#1'}

            payment = client.order.create(data=data)

            rzp_order_id = payment.get('id')

            amount = payment.get('amount')

            Transactions.objects.create(rzp_order_id=rzp_order_id,payment=payment_obj)

            return render(request,'services/razorpay-page.html',context={'rzp_key_id':config('RZP_KEY_ID'),
                                                                     'amount':amount,
                                                                     'rzp_order_id':rzp_order_id})
    
@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        # authenticating razorpay client

        client = razorpay.Client(auth=(config('RZP_KEY_ID'),config('RZP_KEY_SECRET')))

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_signature = request.POST.get('razorpay_signature')

        transaction_obj = Transactions.objects.get(rzp_order_id=rzp_order_id)

        transaction_obj.rzp_payment_id = rzp_payment_id

        transaction_obj.rzp_signature = rzp_signature

        try:

            client.utility.verify_payment_signature(request.POST)

            transaction_obj.txn_status = 'Success'

            transaction_obj.payment.payment_status = 'Success'

            transaction_obj.payment.save()

            transaction_obj.save()

            return render(request,'services/home.html')

        except:

            transaction_obj.txn_status = 'Failed'

            transaction_obj.payment.payment_status = 'Failed'

            transaction_obj.payment.save()

            transaction_obj.save()

            service = request.session['service']

            payment = transaction_obj.payment

            return render(request,'services/payment-page.html',context={'service':service,'payment':payment})



class LoginView(View):

    def get(self,request,*args,**kwargs):

        form = LoginForm()

        return render(request,'services/login.html',context={'form':form})
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():

            user = authenticate(**form.cleaned_data)

            if user :

                login(request,user)

                return redirect('application-list')
            

        error = 'user does not exist'

        return render(request,'services/login.html',context={'form':form,'error':error})
    

class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')
             
@method_decorator(login_required(login_url='login'),name='dispatch')
class ApplicationListView(View):

    def get(self,request,*args,**kwargs):

        service,status = request.GET.get('service'),request.GET.get('status')
            
        if service:

            if service=='New Vehicle Registration':

                all_applications = models.Vehicles.objects.filter()
                 
                if status:

                    all_applications = models.Vehicles.objects.filter(application_status=status)

            elif service=='Registration Renewal':

                all_applications = models.RegistrationRenewal.objects.filter()

                if status:

                    all_applications = models.RegistrationRenewal.objects.filter(application_status=status)

            elif service=='Transfer of Ownership':

                all_applications = models.TransferOfOwnership.objects.filter()

                if status:

                    all_applications = models.TransferOfOwnership.objects.filter(application_status=status)

            elif service=='Learners Licence':

                all_applications = models.LearnersLicence.objects.filter()

                if status:

                    all_applications = models.LearnersLicence.objects.filter(application_status=status)

            elif service=='Driving Licence':

                all_applications = models.DrivingLicence.objects.filter()

                if status:

                    all_applications = models.DrivingLicence.objects.filter(application_status=status)

            elif service=='National Permit':

                all_applications = models.NationalPermit.objects.filter()

                if status:
                    all_applications = models.NationalPermit.objects.filter(application_status=status)

        else:

            if status:

                all_applications = chain(models.Vehicles.objects.filter(application_status=status),
                                      models.RegistrationRenewal.objects.filter(application_status=status),
                                      models.LearnersLicence.objects.filter(application_status=status),
                                      models.DrivingLicence.objects.filter(application_status=status),
                                      models.NationalPermit.objects.filter(application_status=status),
                                      models.TransferOfOwnership.objects.filter(application_status=status)) 
            else:

                all_applications = chain(models.Vehicles.objects.filter(),
                                      models.RegistrationRenewal.objects.filter(),
                                      models.LearnersLicence.objects.filter(),
                                      models.DrivingLicence.objects.filter(),
                                      models.NationalPermit.objects.filter(),
                                      models.TransferOfOwnership.objects.filter())    


        return render(request,'services/application-list.html',context={'all_applications':all_applications,'service':service,'status':status})
    
# function to get object,template,context     
    
def get_service_obj_template(service,uuid):

    if service == 'New Vehicle Registration':

            obj = models.Vehicles.objects.get(uuid=uuid)

            template = 'services/vehicle-registration-details.html'

    elif service == 'Registration Renewal':

            obj = models.RegistrationRenewal.objects.get(uuid=uuid)

            template = 'services/renewal-registration-details.html'

    elif service == 'Transfer of Ownership':

            obj = models.TransferOfOwnership.objects.get(uuid=uuid)

            template = 'services/transfer-of-ownership-details.html'

    elif service == 'Learners Licence':

            obj = models.LearnersLicence.objects.get(uuid=uuid)

            template = 'services/learners-licence-details.html'

    elif service == 'Driving Licence':

            obj = models.DrivingLicence.objects.get(uuid=uuid)

            template = 'services/driving-licence-details.html'

    elif service == 'National Permit':

            obj = models.NationalPermit.objects.get(uuid=uuid)

            template = 'services/national-permit-details.html'

    return obj,template        

class ApplicationDetailView(View):

    def get(self,request,*args,**kwargs):

        service = kwargs.get('service')

        uuid = kwargs.get('uuid')

        obj,template = get_service_obj_template(service,uuid)

        return render(request,template,context={'service_obj':obj})    
    

    def post(self,request,*args,**kwargs):

        service = kwargs.get('service')

        uuid = kwargs.get('uuid')

        status = request.POST.get('status')

        remarks = request.POST.get('remarks')

        if service == 'New Vehicle Registration':

            obj = models.Vehicles.objects.get(uuid=uuid)   

        elif service == 'Registration Renewal':

            obj = models.RegistrationRenewal.objects.get(uuid=uuid)

        elif service == 'Transfer of Ownership':

            obj = models.TransferOfOwnership.objects.get(uuid=uuid)

        elif service == 'Learners Licence':

            obj = models.LearnersLicence.objects.get(uuid=uuid)


        elif service == 'Driving Licence':

            obj = models.DrivingLicence.objects.get(uuid=uuid)


        elif service == 'National Permit':

            obj = models.NationalPermit.objects.get(uuid=uuid)

        if service == 'New Vehicle Registration':

            if status=='Approved':
                
                registration_number = get_registration_number()

                obj.registration_number = registration_number

        obj.application_status=status

        obj.remarks_if_rejected = remarks

        obj.save()

        if service == 'Transfer of Ownership':

            email_1,email_2 = obj.buyer_email,obj.seller_email

            msg=EmailMultiAlternatives('Application Status',from_email=settings.EMAIL_HOST_USER,to=[email_1,email_2])

        else:

            email = obj.email

            msg=EmailMultiAlternatives('Application Status',from_email=settings.EMAIL_HOST_USER,to=[email])  

        html_message=render_to_string('services/approval-rejection.html',{'obj':obj,'service':service})

        msg.attach_alternative(html_message,'text/html')

        thread = threading.Thread(target=send_email,args=(msg,))

        thread.start()

        return redirect('application-list')




class ChasisWithMobView(View):

    def get(self,request,*args,**kwargs):

        form = ChasisWithMobForm()

        return render(request,'services/application-num-with-mob.html',context={'form':form})

    def post(self,request,*args,**kwargs):

        form = ChasisWithMobForm(request.POST)

        if form.is_valid():

            application_number = form.cleaned_data.get('application_number')

            mobile_number = form.cleaned_data.get('mobile_number')


            all_applications = chain(models.Vehicles.objects.filter(application_number=application_number,contact_number=mobile_number),
                                      models.RegistrationRenewal.objects.filter(application_number=application_number,contact_number=mobile_number),
                                      models.LearnersLicence.objects.filter(application_number=application_number),
                                      models.DrivingLicence.objects.filter(application_number=application_number),
                                      models.NationalPermit.objects.filter(application_number=application_number,contact_number=mobile_number),
                                      models.TransferOfOwnership.objects.filter(Q(application_number=application_number)&(Q(seller_contact_number=mobile_number)|Q(buyer_contact_number=mobile_number))) 
                                      
                                      )  
        
            return render(request,'services/application-list-unauthorized.html',context={'all_applications':all_applications})
        
        return render(request,'services/application-num-with-mob.html',context={'form':form})








    




