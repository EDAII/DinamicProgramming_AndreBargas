from django.shortcuts import render
from portal.models import Activity, create_activities, schedul_activities

def home(request):
    new_activities = create_activities(10)
    best_schedual = schedul_activities(new_activities)
    return render(request, 'home.html', {'activities': new_activities, 'schedual': best_schedual})
