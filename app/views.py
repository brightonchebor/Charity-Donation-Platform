from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Campaign
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
def home(request):
    user_org = None
    if request.user.is_authenticated:
        user_org = Organization.objects.filter(owner=request.user).first()
    context = {
        'user_org': user_org,
        'user_authenticated': request.user.is_authenticated 
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

