from django.db import models

import uuid

from multiselectfield import MultiSelectField

from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType

# Create your models here.

class BaseClass(models.Model):

    uuid = models.SlugField(default=uuid.uuid4, unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

# registration status choices

class RegistrationStatusChoices(models.TextChoices):

    PENDING = 'Pending','Pending'

    APPROVED = 'Approved','Approved'

    REJECTED = 'Rejected','Rejected' 

# vehicle registration model 

class Vehicles(BaseClass):
    application_number = models.CharField(max_length=15,unique=True)
    # Vehicle Information
    chasis_number = models.CharField(max_length=17)

    engine_number = models.CharField(max_length=11)

    temp_registration_number = models.CharField(max_length=10)

    manufacturer = models.CharField(max_length=50)

    model = models.CharField(max_length=50)

    variant = models.CharField(max_length=50)

    year_of_manufacture = models.CharField(max_length=4)

    vehicle_class = models.CharField(max_length=50)

    # Owner Information
    owner_name = models.CharField(max_length=50)

    address = models.TextField()

    contact_number = models.CharField(max_length=15)

    email = models.EmailField()

    aadhar_number = models.CharField(max_length=12)

    

    # Insurance Information
    insurance_policy_number = models.CharField(max_length=50)

    policy_provider = models.CharField(max_length=50)

    insurance_expiry_date = models.DateField()

    # Document Uploads
    proof_of_address = models.FileField(upload_to='documents/address')

    document = models.FileField(upload_to='documents/additional',null=True,blank=True)

    pollution_certificate = models.FileField(upload_to='documents/pollution')

    # Registration Information
    
    application_status = models.CharField(max_length=10,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    date_of_registration = models.DateTimeField(null=True,blank=True)

    rto = models.CharField(max_length=50)

    registration_number = models.CharField(max_length=10,null=True,blank=True)


    def __str__(self):

        return f'{self.owner_name}-{self.model}-{self.variant}'

    class Meta:

        verbose_name = "Vehicle Registration"

        verbose_name_plural = "Vehicle Registration"

    
# vehicle renewalregistration model 

class RegistrationRenewal(BaseClass):

    # Vehicle Information

    application_number = models.CharField(max_length=15,unique=True)

    vehicle = models.ForeignKey('Vehicles',on_delete=models.CASCADE)

    chasis_number = models.CharField(max_length=17)

    engine_number = models.CharField(max_length=11)

    registration_number = models.CharField(max_length=10)

    manufacturer = models.CharField(max_length=50)

    model = models.CharField(max_length=50)

    variant = models.CharField(max_length=50)

    year_of_manufacture = models.CharField(max_length=4)

    vehicle_class = models.CharField(max_length=50)

    # Owner Information
    owner_name = models.CharField(max_length=50)

    address = models.TextField()

    contact_number = models.CharField(max_length=15)

    email = models.EmailField()

    aadhar_number = models.CharField(max_length=12)

    date_of_registration = models.DateField()

    rto = models.CharField(max_length=50)

    

    

    # Insurance Information
    insurance_policy_number = models.CharField(max_length=50)

    policy_provider = models.CharField(max_length=50)

    insurance_expiry_date = models.DateField()

    # Document Uploads
    proof_of_address = models.FileField(upload_to='documents/renewal/address')

    document = models.FileField(upload_to='documents/renewal/additional',null=True,blank=True)

    pollution_certificate = models.FileField(upload_to='documents/renewal/pollution')

    # Registration Information
    application_status = models.CharField(max_length=10,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    renewal_expiry_date = models.DateField(null=True,blank=True)

    renewal_registration_expired = models.BooleanField(default=False)



    def __str__(self):

        return f'Renewal-{self.owner_name}-{self.model}-{self.variant}'

    class Meta:

        verbose_name = "Vehicle Registration Renewal"

        verbose_name_plural = "Vehicle Registration Renewal"



class TransferOfOwnership(BaseClass):

    application_number = models.CharField(max_length=15,unique=True)

    # Vehicle Information

    vehicle = models.ForeignKey('Vehicles',on_delete=models.CASCADE)

    # Seller Information
    seller_name = models.CharField(max_length=50)

    seller_address = models.TextField()

    seller_contact_number = models.CharField(max_length=15)

    seller_email = models.EmailField()

    rc_book_doc = models.FileField(upload_to='documents/transferownership/rcbooks')

    pollution_certificate = models.FileField(upload_to='documents/transferownership/pollution')

    insurance_certificate = models.FileField(upload_to='documents/transferownership/insurance')

    seller_proof_of_address = models.FileField(upload_to='documents/transferownership/address')

    seller_proof_of_id = models.FileField(upload_to='documents/transferownership/idproof')

    # Buyer Information

    buyer_name = models.CharField(max_length=50)

    buyer_address = models.TextField()

    buyer_contact_number = models.CharField(max_length=15)

    buyer_email = models.EmailField()

    buyer_proof_of_address = models.FileField(upload_to='documents/transferownership/address')

    buyer_proof_of_id = models.FileField(upload_to='documents/transferownership/idproof')

    date_of_transfer = models.DateField()

    application_status = models.CharField(max_length=15,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    ownership_changed_at = models.DateField(null=True,blank=True)




    def __str__(self):

        return f'Transfer-{self.seller_name}-{self.buyer_name}'

    class Meta:

        verbose_name = "Transfer Of Ownership"

        verbose_name_plural = "Transfer Of Ownership"


class GenderChoices(models.TextChoices):

    MALE = 'Male','Male'

    FEMALE = 'Female','Female'

    OTHER = 'Other','Other'

class VehicleTypeChoices(models.TextChoices):

    TWO_WHEELER_WITH_GEAR = 'Two Wheeler(Gear)','Two Wheeler(Gear)'

    TWO_WHEELER_WITHOUT_GEAR = 'Two Wheeler(Without Gear)','Two Wheeler(Without Gear)'

    LIGHT_MOTOR_VEHICLE = 'Light Motor Vehicle(LMV)','Light Motor Vehicle(LMV)'

    HEAVY_MOTOR_VEHICLE = 'Heavy Motor Vehicle(HMV)','Heavy Motor Vehicle(HMV)'



class LearnersLicence(BaseClass):

    application_number = models.CharField(max_length=15,unique=True)

    # applicant Information
    full_name = models.CharField(max_length=50)

    father_name = models.CharField(max_length=50)

    date_of_bith = models.DateField()

    gender = models.CharField(max_length=8,choices=GenderChoices.choices)

    age = models.CharField(max_length=20)

    email = models.EmailField()

    occupation = models.CharField(max_length=20)

    address = models.TextField()

    type_of_vehicle = MultiSelectField(choices=VehicleTypeChoices.choices)

    physical_fitness = models.FileField(upload_to='documents/learnerslicence/physicalfitness')

    signature = models.FileField(upload_to='documents/learnerslicence/applicantsignature')

    photo = models.FileField(upload_to='documents/learnerslicence/applicantphoto')

    proof_of_address = models.FileField(upload_to='documents/learnerslicence/address')

    proof_of_id = models.FileField(upload_to='documents/learnerslicence/idproof')

    application_status = models.CharField(max_length=15,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    learners_approved_at = models.DateField(null=True,blank=True)

    def __str__(self):

        return f'Learners-{self.full_name}'

    class Meta:

        verbose_name = "Learner's Licence"

        verbose_name_plural = "Learner's Licence"


class DrivingLicence(BaseClass):

    application_number = models.CharField(max_length=15,unique=True)

    # applicant Information
    full_name = models.CharField(max_length=50)

    father_name = models.CharField(max_length=50)

    date_of_bith = models.DateField()

    gender = models.CharField(max_length=8,choices=GenderChoices.choices)

    age = models.CharField(max_length=20)

    occupation = models.CharField(max_length=20)

    email = models.EmailField()    

    address = models.TextField()

    type_of_vehicle = MultiSelectField(choices=VehicleTypeChoices.choices)

    physical_fitness = models.FileField(upload_to='documents/driving-licence/physicalfitness')

    signature = models.FileField(upload_to='documents/driving-licence/applicant-signature')

    photo = models.FileField(upload_to='documents/driving-licence/applicant-photo')

    proof_of_address = models.FileField(upload_to='documents/driving-licence/address')

    proof_of_id = models.FileField(upload_to='documents/driving-licence/idproof')

    learners_number = models.CharField(max_length=20)

    learners_licence =  models.FileField(upload_to='documents/learnerslicence/learner-licence')

    application_status = models.CharField(max_length=15,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    driving_licence_approved_at = models.DateField(null=True,blank=True)

    def __str__(self):

        return f'Learners-{self.full_name}'

    class Meta:

        verbose_name = "Driving Licence"

        verbose_name_plural = "Driving Licence"


class NationalPermit(BaseClass):

    application_number = models.CharField(max_length=15,unique=True)

    # Vehicle Information

    vehicle = models.ForeignKey('Vehicles',on_delete=models.CASCADE)

    # applicant Information

    vehicle_type = models.CharField(max_length=20)

    full_name = models.CharField(max_length=50)

    address = models.TextField()

    contact_number = models.CharField(max_length=15)

    email = models.EmailField()

    routes = models.TextField()

    rc_book_doc =  models.FileField(upload_to='documents/nationalpermit/rcbooks')

    insurance_certificate =  models.FileField(upload_to='documents/nationalpermit/insurance')

    pollution_certificate =  models.FileField(upload_to='documents/nationalpermit/pollution')

    physical_fitness =  models.FileField(upload_to='documents/nationalpermit/physicalfitness')

    application_status = models.CharField(max_length=15,choices=RegistrationStatusChoices.choices,default=RegistrationStatusChoices.PENDING)

    remarks_if_rejected = models.TextField(null=True,blank=True)

    permit_approved_at = models.DateField(null=True,blank=True)

    def __str__(self):

        return f'National Permit-{self.full_name}'

    class Meta:

        verbose_name = "National Permit"

        verbose_name_plural = "National Permit"

class FeeChoices(models.IntegerChoices):

    VEHICLE_REGISTRATION_OR_LEARNERS_LICENCE = 1500,'1500'

    RENEWAL_VEHICLE_REGISTRATION =1200,'1200'

    TRANSFER_OF_OWNERSHIP = 1000,'1000'

    DRIVING_LICENCE = 2000,'2000'

    NATIONAL_PERMIT = 2500,'2500' 

class PaymentStatusChoices(models.TextChoices):

    SUCCESS = 'Success','Success'

    PENDING = 'Pending','Pending'

    FAILED = 'Failed','Failed'


class Payments(BaseClass):

    txn_id = models.BigIntegerField()
    
    service_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL,null=True)

    service_id = models.PositiveIntegerField()

    service = GenericForeignKey('service_type', 'service_id')

    fee = models.IntegerField(choices=FeeChoices.choices)

    payment_status = models.CharField(max_length=10,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    def __str__(self):

        return f'Payment-{self.service}'

    class Meta:

        verbose_name = "Payments"

        verbose_name_plural = "Payments"


class Transactions(BaseClass):

    payment = models.ForeignKey('Payments',on_delete=models.SET_NULL,null=True) 

    rzp_order_id = models.SlugField(null=True)

    rzp_payment_id = models.SlugField(null=True)

    rzp_signature = models.TextField(null=True)

    txn_status = models.CharField(max_length=15,default=PaymentStatusChoices.PENDING)

    def __str__(self):

        return f'Transaction-{self.payment.service}-{self.rzp_order_id}'

    class Meta:

        verbose_name = "Transactions"

        verbose_name_plural = "Transactions"

    










    
