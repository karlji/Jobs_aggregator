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
    context = {
        'jobs_total': jobs_total,
    }
    return HttpResponse(template.render(context, request))
