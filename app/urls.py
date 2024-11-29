from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('create-campaign/', create_campaign, name='create-campaign'),
    path('regiter-org/', register_org, name='register-org')
]
