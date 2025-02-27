from django.urls import path

from . import views

urlpatterns =[
    path('registration-number/',views.RegistrationNumberView.as_view(),name='registration-number'),

    path('registration-with-chasis/',views.RegistrationNumberWithChasisView.as_view(),name='registration-with-chasis'),

    path('vehicle-registration/',views.VehicleRegistrationView.as_view(),name='vehicle-registration'),

    path('renewal-registration/',views.RegistrationRenewalView.as_view(),name='renewal-registration'),

    path('transfer-ownership/',views.TransferOfOwnershipView.as_view(),name='transfer-ownership'),

    path('learners-licence/',views.LearnersLicenceView.as_view(),name='learners-licence'),

    path('driving-licence/',views.DrivingLicenceView.as_view(),name='driving-licence'),

    path('national-permit/',views.NationalPermitView.as_view(),name='national-permit'),

    path('payment/',views.PaymentView.as_view(),name='payment'),

    path('payment-verification/',views.PaymentVerificationView.as_view(),name='payment-verification'),

    path('login/',views.LoginView.as_view(),name='login'),

    path('logout/',views.LogoutView.as_view(),name='logout'),

    path('application-list/',views.ApplicationListView.as_view(),name='application-list'),

    path('application-details/<str:service>/<str:uuid>/',views.ApplicationDetailView.as_view(),name='application-details'),

    path('chasis-mob/',views.ChasisWithMobView.as_view(),name='chasis-mob'),

    
]