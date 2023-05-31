from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Job
from jobs_scraper import scrape_data,clean_data
from django.shortcuts import redirect
from .forms import JudgesForm
from django.contrib.auth import authenticate
from django.contrib import messages
from BruteBuster.models import FailedAttempt #BB needs edit to return False in decorators.py when calling fa.too_many_failures():
from datetime import timedelta

# Create your views here.
def home_view(request):
    # Initiate your form
    judge_form = JudgesForm(request.POST or None)
    # Initiate your session variable
    request.session['judge_password'] = 'invalid'
    if (request.method == 'POST'):
        if judge_form.is_valid():
            user = judge_form.cleaned_data['username']
            password = judge_form.cleaned_data['password']
            try:
                auth = authenticate(username=user, password=password)# Authenticate is change with BruteBuster lib, which tracks failed login attempts into DB.
                if auth == False: # when max attempts failed, block user
                    IP_ADDR = request.META.get('REMOTE_ADDR', None)
                    fa = FailedAttempt.objects.filter(username=user, IP=IP_ADDR)[0]
                    block_time = (fa.timestamp + timedelta(minutes=3)).strftime('%H:%M:%S')
                    messages.info(request, u'%s BLOCKED until %s GMT' % (fa.username,  block_time))
                if auth != None and auth != False:
                    request.session['judge_password'] = 'valid'
                    return redirect('search')
                else:
                    return redirect('home_view')
            except:
                print("Failed")
                # handle exceptions here """ """
    return render(request, "home.html", {'judge_form': judge_form})

def index(request):
    try:
        if (request.session['judge_password'] != 'valid'):
            return redirect('home_view')
    except:
        return redirect('home_view')
        
    jobs_total = Job.objects.all().values()
    template = loader.get_template('jobs_dashboard/index.html')
    input_text = request.POST.get('my_input', None)
    junior_check = request.POST.get('junior_check', None)
    salary_check = request.POST.get('salary_check', None)
    city_check = request.POST.get('city_check', None)

    if junior_check == "on":
        junior_check = "junior"
    else:
        junior_check = ""

    if salary_check == "on":
        salary_check = "Kč"
    else:
        salary_check = ""

    if input_text == None:
        input_text = ""

    context = {
        'jobs_total': jobs_total,
        'input_text': input_text,
        'junior_check': junior_check,
        'salary_check': salary_check,
        'city_check': city_check
        
    }
    return HttpResponse(template.render(context, request))


def search(request):
    try:
        if (request.session['judge_password'] != 'valid'):
            return redirect('home_view')
    except:
        return redirect('home_view')

    template = loader.get_template('jobs_dashboard/search.html')
    input_text = request.POST.get('my_input', None)
    city_check = request.POST.get('city_check', None)
    context = {
        'city_check': city_check
        
    }
    if city_check == None: #On first page load render search.html
        return HttpResponse(template.render(context, request))
    else:
        clean_data()
        scrape_data(city_check,input_text)
        return redirect('/dashboard/view')
    
