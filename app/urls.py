from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('create-campaign/<int:organization_id>/', create_campaign, name='create-campaign'),
    path('register-org/', register_org, name='register-org'),
    path('about/', about, name='about'),
    path('view-campaigns/', view_campaigns, name='view-campaigns'),
    path('view-campaign/<int:id>/', campaign_details, name='campaign-details'),
    path('stk/<int:id>/', stk, name='stk'),
    path('my-campaign/<int:id>/', my_campaign, name='my-campaign'),
    path('download-transactions/<int:id>/', download_csv, name='download-csv'),
    path('delete-campaign/<int:id>/', delete_campaign, name='delete-campaign'),
    path('edit_campaign/<int:id>/', edit_campaign, name='edit-campaign'),
   
]
