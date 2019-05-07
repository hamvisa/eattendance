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
                attendance_records = Attendance.objects.filter(student=student).order_by('-timestamp')
            except ObjectDoesNotExist:
                return HttpResponse("Error fetching student records for user: " + str(user))
            return render(request=request, template_name='student/home.html',
                          context={'student': student, 'attendance_records' : attendance_records})   #To-do when errors are checked for

        else:
            return HttpResponse("User type: " + str(type) + " cannot access Student Portal.")
    else:
        return HttpResponse("Please Log-In to continue.")
