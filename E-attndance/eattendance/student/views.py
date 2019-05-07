from django.shortcuts import render
from django.http import HttpResponse
from database.models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            type = request.session['type']
            user = request.user
        except:
            return HttpResponse("User object can not be accessed")
        if type == 'student':
            try:
                student = Student.objects.get(pk=user)
            except ObjectDoesNotExist:
                return HttpResponse("Error fetching student records for user: " + str(user))
            return render(request=request, template_name='student/home.html',
                          context={'student': student, })   #To-do when errors are checked for

        else:
            return HttpResponse("User type: " + str(type) + " cannot access Student Portal.")
    else:
        return HttpResponse("Please Log-In to continue.")
