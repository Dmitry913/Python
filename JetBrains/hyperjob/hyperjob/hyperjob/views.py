from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from django.contrib.auth.models import User
from resume.models import Resume
from vacancy.models import Vacancy
from django.http import HttpResponseForbidden


class MainView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'Main_page.html')


class MySignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class HomePage(View):
    def get(self, request, *args, **kwarg):
        return render(request, 'Home_page.html')

    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        if request.user.is_authenticated and not request.user.is_staff:
            Resume.objects.create(description=description, author=request.user)
            return redirect('/home')
        elif request.user.is_authenticated and request.user.is_staff:
            Vacancy.objects.create(description=description, author=request.user)
            return redirect('/home')
        else:
            return HttpResponseForbidden()
