from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm


# Create your views here.

###
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request, user)

#             return redirect('frontpage')
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'accounts/signup.html', {'form': form})


# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#             'form':form,
#     }
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         new_user = User.objects.create_user(username, email, password)
#         return redirect('login')
#     return render(request, "accounts/signup.html", context)


###
# def login_page(request):
#     form_class = LoginForm(request.POST or None)
#     context = {
#             'form':form_class,
#     }
#     if form_class.is_valid():
#         user = form_class.cleaned_data.get('username')
#         password = form_class.cleaned_data.get('password')
#         user = authenticate(request,
#                             user=user,
#                             password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             print("Error you are not loged in yet check this error")
#             return redirect("login")
#     return render(request, "accounts/login.html", context)
