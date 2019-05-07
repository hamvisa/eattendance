from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from database.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def my_login(request):
    if request.method == 'POST':
            email_id = request.POST['email_id']
            password = request.POST['password']
            user = authenticate(request=request, username=email_id, password=password)
            if user is not None:
                    try:
                        student = Student.objects.get(pk=user)
                        logout(request)
                        request.session['type'] = 'student'
                        login(request, user)
                        return redirect('student:home')
                    except ObjectDoesNotExist:
                        pass
                    try:
                        faculty = Faculty.objects.get(pk=user)
                        logout(request)
                        request.session['type'] = 'faculty'
                        login(request, user)
                        return redirect('faculty:home')
                    except ObjectDoesNotExist:
                        pass
                    try:
                        admin = Admin.objects.get(pk=user)
                        logout(request)
                        request.session['type'] = 'admin'
                        login(request, user)
                        return redirect('/admin')
                    except ObjectDoesNotExist:
                        pass
                    return HttpResponse("User type not found.")
            else:
                return HttpResponse("User with that credentials was not found")
    else:
        # return render(request=request, template_name='authenticate/login.html', context={'form': form, 'type': type, })
        return redirect('home:index')


def my_logout(request):
    logout(request)
    return HttpResponse("Logged out. ")


def my_change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponse("Password Changed.")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'authenticate/change_password.html', {'form': password_change_form, })


def password_reset_confirm(request, uidb64, token):
    return redirect('authenticate:password_reset_confirm', uidb64=uidb64, token=token)


def password_reset_complete(request):
    return redirect('authenticate:password_reset_complete')


def password_reset_done(request):
    return redirect('authenticate:password_reset_done')
