from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('create-campaign/<int:organization_id>/', create_campaign, name='create-campaign'),
    path('register-org/', register_org, name='register-org'),
    path('about/', about, name='about'),
    path('view-campaigns/', view_campaigns, name='view-campaigns')
   
]
