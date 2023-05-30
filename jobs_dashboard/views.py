from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Job
from jobs_scraper import scrape_data,clean_data
from django.shortcuts import redirect


# Create your views here.
def greet(request, name):
    return render(request, "jobs_dashboard/greet.html", {
        "name": name
    })


def index(request):
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
    template = loader.get_template('jobs_dashboard/search.html')
    city_check = request.POST.get('city_check', None)
    context = {
        'city_check': city_check
        
    }
    if city_check == None: #On first page load render search.html
        return HttpResponse(template.render(context, request))
    else:
        clean_data()
        scrape_data()
        return redirect('/dashboard/view')
    
