from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Campaign, Transaction
from django.contrib import messages

import requests
import json
from .credentials import LipanaMpesaPpassword, MpesaAccessToken

from django.http import HttpResponse
from django.utils.timezone import now
import csv

def home(request):
    
    user_org = None
    if request.user.is_authenticated:
        user_org = Organization.objects.filter(owner=request.user).first()
    context = {
        'user_org': user_org,
        'user_authenticated': request.user.is_authenticated,
    }
    return render(request,'app/home.html', context)


def create_campaign(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id, owner=request.user)    

    if request.method == 'POST':

        title = request.POST['title']
        image = request.FILES['image']
        goals_and_plans = request.POST['goals_and_plans']
        title = request.POST['title']
        goal_amount = request.POST['goal_amount'] 

        new_campaign = Campaign.objects.create(
            goals_and_plans = goals_and_plans,
            goal_amount = goal_amount,
            image = image,
            organization = organization,
            title = title
        )
        messages.success(request, 'Your Campaign has been created successfully.')
        return redirect('app:home')

    context = {
        'organization':organization
    }

    return render(request, 'app/create_campaign.html', context)

@login_required(login_url='accounts:login')
def register_org(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        owner = request.user

        new_org = Organization.objects.create(
            name=name, description=description, owner=owner
        )
        new_org.save()
        messages.success(request, 'Your Organization has been created successfully, proceed and create a campaign')
        return redirect('app:home')
        
    context = {}

    return render(request, 'app/register_org.html', context)

def about(request):
    context =  {

    }
    
    return render(request, 'app/about.html', context)

def view_campaigns(request):
    campaigns = Campaign.objects.all()
    context = {
        'campaigns': campaigns
    }
    return render(request, 'app/view_campaigns.html', context)

def campaign_details(request, id):
    
    return render(request, 'app/campaign_details.html')

def delete_campaign(request, id):
    campaign = Campaign.objects.get(id=id)
    if request.method == 'POST':
        campaign.delete()  
        messages.success(request, 'Campaign deleted successfully') 
        return redirect('app:view-campaigns')
    context = {
        'campaign': campaign
    }  

    return render(request, 'app/delete_campaign.html')    

def my_campaign(request, id):
    try:
        campaign = get_object_or_404(Campaign, id=id)

        context = {
            'campaign': campaign
        }    
        return render(request, 'app/my_campaign.html', context)
    
    except:
        messages.error(request, 'No Campaign matches the given query')
        return redirect('app:home')




def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'qvQFfRUmIIMKcLutXyGEdAbkKtYN7RzIjVKiMz8Ma94qQt4q'
    consumer_secret = 'HRSVAAGk1AEG4ZATjzWmqYSTpGluFG6Erf8gRab85NEepozIGSmTPmR6k2Cu9Ivr'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    organization = campaign.organization

    """ Sends the stk push prompt """
    if request.method =="POST":
        donor_phone = request.POST['donor_phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": donor_phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": donor_phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "charifit",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        response_data = response.json()

        transaction = Transaction.objects.create(
            transaction_id=response_data.get("CheckoutRequestID"),
            donor_phone=donor_phone,
            amount=amount,
            transaction_time=now(),
            status="Approved", # to be updated by callback
            organization = organization,
            campaign = campaign
        )
       
        # return HttpResponse("Thank you for your generosity! Your donation has been successfully initiated. 😊")
        messages.success(request, 'Thank you for your generosity! Your donation has been successfully initiated. 😊')
        return redirect('app:view-campaigns')
    
def download_csv(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    transactions = campaign.transactions.all()

    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = f'attachment; filename="{campaign.title}_transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Transaction ID', 'Donor Phone', 'Amount', 'Transaction Time'])
    for transaction in transactions: 
        writer.writerow([transaction.transaction_id, transaction.donor_phone, transaction.amount, transaction.transaction_time]) 
    return response