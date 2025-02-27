import uuid

from . import models

import random

import string

def get_vehicle(reg_num,chsis_num):

    try :

        vehicle = models.Vehicles.objects.get(registration_number=reg_num,chasis_number__endswith=chsis_num)

    except models.Vehicles.DoesNotExist:

        vehicle = None

    return vehicle

def get_application_number():
     

     while True :
          
          application_number = str(uuid.uuid4().int)[:15]    

          object_exists = ( 
                            models.Vehicles.objects.filter(application_number=application_number).exists() or
                           
                            models.RegistrationRenewal.objects.filter(application_number=application_number).exists() or

                            models.TransferOfOwnership.objects.filter(application_number=application_number).exists() or

                            models.LearnersLicence.objects.filter(application_number=application_number).exists() or

                            models.DrivingLicence.objects.filter(application_number=application_number).exists() or

                            models.NationalPermit.objects.filter(application_number=application_number).exists()

                           )
          
          if not object_exists:
               
               return application_number
          

def get_txn_id():
     
     
     while True:
          
          txn_id = str(uuid.uuid4().int)[:10]
          
          if not models.Payments.objects.filter(txn_id=txn_id).exists():
               
               return txn_id
          
          
def get_registration_number():

    while True: 

        district_code = f"{random.randint(1, 99):02d}"

        alphabetic_code = ''.join(random.choices(string.ascii_uppercase, k=2))

        number = f"{random.randint(0, 9999):04d}"

        registration_number = f'KL{district_code}{alphabetic_code}{number}'  

        if not models.Vehicles.objects.filter(registration_number=registration_number).exists():

             return registration_number  
        

def get_learners_number():

    while True: 

        number = f"{random.randint(0, 999999999):09d}"

        learners_number = f'LRN{number}'  

        if not models.LearnersLicence.objects.filter(learners_number=learners_number).exists():

             return learners_number  
        

def send_email(msg):

     msg.send()        


               

                            

