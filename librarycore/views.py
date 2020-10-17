from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .mixins import UserIsAdminMixin

