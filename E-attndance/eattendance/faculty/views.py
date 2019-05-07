from django.shortcuts import render
from django.http import HttpResponse
from database.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            type = request.session['type']
            user = request.user
        except:
            return HttpResponse("User object can not be accessed")
        if type == 'faculty':
            try:
                faculty = Faculty.objects.get(
                    pk=user)  # <Faculty: 1620150001    Manish Potey    manish.potey@somaiya.edu, B-108, Computer Engineering>
                schedules = Schedule.objects.filter(faculty=faculty)
                ''' <QuerySet [<Schedule: MON: 11:30:00-12:30:00. COMPS, LY, B, FC by: MMP Sub:DCC>, <Schedule: THU: 14:15:00-15:15:00. COMPS, LY, B, FC by: MMP Sub:DCC>, <Schedule: WED: 11:30:00-12:30:00. COMPS, TY, A, FC b
y: MMP Sub:DN>]>*/ '''
                subjects = set()
                students_attendnce_records = set()
                for schedule in schedules:
                    subjects.add(schedule.subject)
                    attendance_records = Attendance.objects.filter(schedule=schedule)
                    for attendance_record in attendance_records:
                        students_attendnce_records.add(attendance_record)
                # subjects contain all subject objects taught by faculty
            except ObjectDoesNotExist:
                return HttpResponse("Error fetching faculty records for user: " + str(user))
            return render(request=request, template_name='faculty/home.html',
                          context={'faculty': faculty, 'subjects': subjects, 'students_attendance_records' : students_attendnce_records})

        else:
            return HttpResponse("User type: " + str(type) + " cannot access Faculty Portal.")
    else:
        return HttpResponse("Please Log-In to continue.")
