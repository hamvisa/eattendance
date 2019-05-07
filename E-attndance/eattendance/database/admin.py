from django.contrib import admin
from database.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from database.forms import *


class PersonAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id', 'first_name', 'last_name', 'phone_number', 'email_id', 'password', 'profile_picture', 'training_dataset',
        'user_since',
        'is_active', 'is_superuser',)
    list_filter = ('is_superuser', 'is_active', 'user_since',)
    fieldsets = (
        (None, {'fields': ('email_id', 'password')}),
        ('Personal info', {'fields': (
            'id', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'training_dataset',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email_id', 'password1', 'password2',)}),
        ('Personal info', {'fields': (
            'id', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'training_dataset',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('email_id', 'id', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ()


class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'acronym', 'year',)
    ordering = ('id',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'acronym', 'name')
    search_fields = ('name',)
    ordering = ('id',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'initials', 'year', 'department',)
    list_filter = ('year', 'department')
    search_fields = ('code', 'name', 'initials',)
    ordering = ('code',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'year', 'division', 'batch', 'department',)
    list_filter = ('department', 'year', 'division', 'batch',)
    search_fields = (
    'person__id', 'person__first_name', 'person__last_name', 'person__phone_number', 'person__email_id',)
    ordering = ('person',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('person', 'room_number', 'department',)
    search_fields = (
    'person__id', 'person__first_name', 'person__last_name', 'person__phone_number', 'person__email_id',)
    ordering = ('person',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class AdminAdmin(admin.ModelAdmin):
    list_display = ('person',)
    search_fields = (
    'person__id', 'person__first_name', 'person__last_name', 'person__phone_number', 'person__email_id',)
    ordering = ('person',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
    'day', 'beginning_time', 'ending_time', 'department', 'year', 'division', 'batch', 'facultyName', 'subjectName',)
    ordering = ('day', 'beginning_time', 'ending_time', 'department', 'year', 'division', 'batch',)
    search_fields = (
    'faculty__initials', 'subject__initials', 'faculty__person__first_name', 'faculty__person__last_name',
    'subject__name', 'subject__code',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'schedule', 'student', 'present', 'concession', 'modified',)
    list_filter = ('timestamp', 'present', 'concession', 'modified',)

    ordering = ('timestamp',)
    search_fields = ()
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()

class CameraAdmin(admin.ModelAdmin):
    list_display = ('lecture_class', 'url',)
    list_filter = ()

    ordering = ('lecture_class',)
    search_fields = ('lecture_class',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    filter_horizontal = ()

admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Camera, CameraAdmin)

admin.site.unregister(Group)

# Register your models here.
