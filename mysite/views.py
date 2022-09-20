from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def index(request):
    """Redirect to index page for empty url"""
    return redirect('polls:index')
