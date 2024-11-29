from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Organization
from django.contrib import messages

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

def create_campaign(request):
    context = {}

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
        messages.success(request, 'Your Organization has been created successfully, procced and create a campaign')
        return redirect('app:create-campaign')
        
    context = {}

    return render(request, 'app/register_org.html', context)

