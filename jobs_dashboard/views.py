from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Job


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

    if junior_check == "on":
        junior_check = "junior"
    else:
        junior_check = ""
    if salary_check == "on":
        salary_check = ""
    else:
        salary_check = "N/A"

    context = {
        'jobs_total': jobs_total,
        'input_text': input_text,
        'junior_check': junior_check,
        'salary_check': salary_check
    }
    return HttpResponse(template.render(context, request))


def search(request):
    template = loader.get_template('jobs_dashboard/search.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
