from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.text import slugify
from .models import Campaign

def get_sanitized_filename(file):
    original_filename = file.name
    name, extension = original_filename.rsplit('.', 1)
    sanitized_name = slugify(name)
    return f"{sanitized_name}.{extension}"

def create_campaign(request):
    if request.method == 'POST':
        image_pic = request.FILES.get('image')
        
        if image_pic:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(get_sanitized_filename(image_pic), image_pic)
            file_url = fs.url(filename)
        
        goals_and_plans = request.POST['goals_and_plans']
        title = request.POST['title']
        goal_amount = request.POST['goal_amount']

        campaign = Campaign.objects.create(
            image=file_url,
            goals_and_plans=goals_and_plans,
            title=title,
            goal_amount=goal_amount
        )
        campaign.save()

        return redirect('some_view')
    else:
        return render(request, 'your_template.html')
