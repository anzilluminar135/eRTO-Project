
from django import forms

import re

from .models import Vehicles,RegistrationRenewal,TransferOfOwnership,LearnersLicence,GenderChoices,VehicleTypeChoices,DrivingLicence,NationalPermit

class RegistrationNumberForm(forms.Form):

    registration_number = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'Enter Registration Number','class':'form-control','id':'registration-number'}))

    def clean(self):

        cleaned_data = super().clean()

        registration_number = cleaned_data.get('registration_number')

        pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$"

        if not re.match(pattern,registration_number):

            self.add_error('registration_number','invalid registration number')
        
        return cleaned_data
    

    
class RegistrationWithChasisForm(forms.Form):

    chasis_number = forms.CharField(max_length=5,widget=forms.TextInput(attrs={'placeholder':'Enter last 5 digits of chasis number','class':'form-control'}))  

    def clean(self):

        cleaned_data = super().clean()

        chasis_number = cleaned_data.get('chasis_number')

        if len(chasis_number)<5:

            self.add_error('chasis_number','input last 5 digits of chasis number ')
        
        return cleaned_data 



class VehicleRegistrationForm(forms.ModelForm):


    class Meta:

        model=  Vehicles

        exclude = ['uuid','active_status','application_status','date_of_registration','registration_number','remarks_if_rejected','application_number'] 

        widgets ={
                    'chasis_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'engine_number' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'temp_registration_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'manufacturer' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'  
                    }) ,


                    'model':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,


                    'variant' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,


                    'year_of_manufacture':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required',
                    }) ,

                    'vehicle_class':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    # Owner Information
                    'owner_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4

                    }) ,


                    'contact_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,


                    'aadhar_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    

                    # Insurance Information
                    'insurance_policy_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'policy_provider':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'insurance_expiry_date':forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    # Document Uploads
                    'proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'document':forms.FileInput(attrs={
                        'class':'form-control'
                    }) ,


                    'pollution_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'rto':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) 

        }
    def clean(self):

        cleaned_data = super().clean()

        aadhar_number = cleaned_data.get('aadhar_number')

        if len(aadhar_number)<12:

            self.add_error('aadhar_number','aadhar number must be 12 digits')
        
        return cleaned_data    

class RenewalRegistrationForm(forms.ModelForm):

    class Meta:

        model=  RegistrationRenewal

        exclude = ['uuid','active_status','vehicle','application_status','application_number'] 

        widgets ={
                    'chasis_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required',
                        'readonly':'readonly'
                    }) ,

                    'engine_number' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required',
                        'readonly':'readonly'
                    }) ,

                    'registration_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required',
                        'readonly':'readonly'
                    }) ,

                    'manufacturer' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'  
                    }) ,


                    'model':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,


                    'variant' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,


                    'year_of_manufacture':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required',
                    }) ,

                    'vehicle_class':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    # Owner Information
                    'owner_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4

                    }) ,


                    'contact_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,


                    'aadhar_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'date_of_registration':forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'rto':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    

                    # Insurance Information
                    'insurance_policy_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'policy_provider':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'insurance_expiry_date':forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    # Document Uploads
                    'proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,


                    'document':forms.FileInput(attrs={
                        'class':'form-control'
                    }) ,


                    'pollution_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) 

                    

        }

    def clean(self):

        cleaned_data = super().clean()

        aadhar_number = cleaned_data.get('aadhar_number')

        if len(aadhar_number)<12:

            self.add_error('aadhar_number','aadhar number must be 12 digits')
        
        return cleaned_data        


class TransferOfOwnershipForm(forms.ModelForm):

    class Meta:

        model=  TransferOfOwnership

        exclude = ['uuid','active_status','vehicle','application_status','application_number'] 

        widgets ={
                    'seller_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'seller_address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4

                    }) ,

                    'seller_contact_number' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                     'seller_email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                    'rc_book_doc':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'pollution_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'insurance_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'seller_proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'seller_proof_of_id':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'buyer_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'buyer_address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4

                    }) ,

                    'buyer_contact_number' :forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                     'buyer_email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                    'buyer_proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'buyer_proof_of_id':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'date_of_transfer':forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required' 
                    })             

        }


class LearnersLicenceForm(forms.ModelForm):

    class Meta:

        model=  LearnersLicence

        exclude = ['uuid','active_status','application_status','application_number'] 

        widgets ={
                    'full_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'father_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 

                    }) ,

                    'date_of_bith' :forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required',
                        'id':'id_date_of_birth'
                    }) ,

                     'age':forms.TextInput(attrs={
                        'class':'form-control' ,
                        'readonly':'readonly',
                        'id':'id_age'
                    }) ,

                    'occupation':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4
                    }) ,

                    'email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                    'physical_fitness':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'signature':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'photo':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'proof_of_id':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) 
        }  

    gender = forms.ChoiceField(choices=GenderChoices.choices,widget=forms.RadioSelect(attrs={
                                                                                       'class':'form-check-input',
                                                                                       'required':'required'
                                                                                        }))  
    
    type_of_vehicle = forms.MultipleChoiceField(choices=VehicleTypeChoices.choices,widget=forms.CheckboxSelectMultiple(attrs={

                                                                                                                            'class':'form-check-input'
    

                                                                                                                            }))




class DrivingLicenceForm(forms.ModelForm):

    class Meta:

        model=  DrivingLicence

        exclude = ['uuid','active_status','application_status','application_number'] 

        widgets ={
                    'full_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'father_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 

                    }) ,

                    'date_of_bith' :forms.DateInput(attrs={
                        'type':'date',
                        'class':'form-control',
                        'required': 'required',
                        'id':'id_date_of_birth'
                    }) ,

                     'age':forms.TextInput(attrs={
                        'class':'form-control' ,
                        'readonly':'readonly',
                        'id':'id_age'
                    }) ,

                    'occupation':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4
                    }) ,

                    'email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                    'physical_fitness':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'signature':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'photo':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'proof_of_address':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'proof_of_id':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'learners_number':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'learners_licence':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) 
        }  

    gender = forms.ChoiceField(choices=GenderChoices.choices,widget=forms.RadioSelect(attrs={
                                                                                       'class':'form-check-input',
                                                                                       'required':'required'
                                                                                        }))  
    
    type_of_vehicle = forms.MultipleChoiceField(choices=VehicleTypeChoices.choices,widget=forms.CheckboxSelectMultiple(attrs={

                                                                                                                            'class':'form-check-input'

                                                                                                                            }))
    
class NationalPermitForm(forms.ModelForm):

    class Meta:

        model=  NationalPermit

        exclude = ['uuid','active_status','application_status','vehicle','application_number'] 

        widgets ={
                    'vehicle_type':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'full_name':forms.TextInput(attrs={
                        'class':'form-control',
                        'required': 'required' 

                    }) ,

                    'address':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4
                    }) ,

                     'contact_number':forms.TextInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                     'email':forms.EmailInput(attrs={
                        'class':'form-control' ,
                        'required':'required'
                    }) ,

                    'routes':forms.Textarea(attrs={
                        'class':'form-control',
                        'required': 'required' ,
                        'cols':70,
                        'rows':4
                    }) ,        

                    'rc_book_doc':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,
                    'insurance_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required' 
                    }) ,

                    'pollution_certificate':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) ,

                    'physical_fitness':forms.FileInput(attrs={
                        'class':'form-control',
                        'required': 'required'
                    }) 
        }  



class LoginForm(forms.Form):

    username = forms.CharField(max_length=5,widget=forms.TextInput(attrs={'placeholder':'Enter Username','class':'form-control','required':'required'})) 
    
    password = forms.CharField(max_length=5,widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control','required':'required'})) 



class ChasisWithMobForm(forms.Form):

    application_number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder':'Enter application number','class':'form-control'}))

    mobile_number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder':'Enter your mobile number','class':'form-control'}))  






