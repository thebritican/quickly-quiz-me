from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from quizapp.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm


#################################  Registration  #################################

def logout(request):
    auth_logout(request)
    return redirect("/")


def login(request, template_name='login.html'):
    message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect("/")
                else:
                    message = "Your account has been disabled!"
                    form = LoginForm()
            else:
                message = "Your username and password were incorrect."
    else:
        form = LoginForm()

    return render(request, template_name, {'form':form, 'message':message})


@login_required
def index(request):
    if user.is_staff:
        return redirect(reverse('quizapp.views.admin_dashboard'))
    else:
        return redirect(reverse('quizapp.views.quiz_dashboard'))

@login_required
def change_password(request, template_name='change_password.html'):
    change_password_form = PasswordChangeForm(request.user)
    message = ''

    if request.POST:
        change_password_form = PasswordChangeForm(request.user, data=request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            message = 'Your password has been changed.'

    return render(request, template_name, {'change_password_form':change_password_form, 'message': message})


#################################  Quiz Views  #################################

@login_required
def quiz_dashboard(request, template_name='quiz/dashboard.html'):
    return render(request, template_name, {})



#################################  Admin Views  #################################


@permission_required('quizuser.is_staff')
def admin_dashboard(request, template_name='admin/dashboard.html'):
    return render(request, template_name, {})