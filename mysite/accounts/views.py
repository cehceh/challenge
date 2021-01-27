from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm


# Create your views here.
