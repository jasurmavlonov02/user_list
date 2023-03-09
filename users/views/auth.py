from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from users.forms import LoginForm
from users.models import Profile


class LoginMixin:

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_list')
        return super().get(request, *args, **kwargs)


class LoginPage(LoginMixin, LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('user_list')


# def login_page(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         # password = make_password(password)
#
#         user = authenticate(request, email=email, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('user_list')
#         else:
#             messages.info(request, 'Email or Password incorrect')
#
#     return render(request, 'auth/login.html')


def logout_page(request):
    logout(request)
    return render(request, 'auth/logout.html')



#jasur