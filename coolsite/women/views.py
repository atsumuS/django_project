from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .forms import *
from .models import *
from .utils import *

# класс представления главной страницы
class WomenHome(DataMixin, ListView):
    model = Women  # откуда берется информация
    template_name = 'women/index.html'  # необходимый атрибут
    context_object_name = 'posts'  # задаем своё имя для {object_name}
    # при помощи {extra_context} можно передовать только статические данные

    # чтобы передовать динамический и статический контекст организовывают специальную функцию
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная Странциа')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')
        # фильтрация по опубликованным постам
        # если пост опубликован, то он выводится


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # переносит на домашнюю страницу при удачном создании статьи
    success_url = reverse_lazy('home')
    # переносит на домащнюю страницу когда пользваотель не зарегистрирован
    login_url = reverse_lazy('Login')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))



# TODO
class loginuser(DataMixin, LoginView):
    template_name = 'women/login.html'
    form_class = loginuserform

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

# TODO


class RegistrationUser(DataMixin, CreateView):
    form_class = RegisterUserForm  # форма для регистрации указана в utils.py
    template_name = 'women/register.html'  # шаблон для отображения на сайте


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    

#TODO нужно доделать этот класс представления 
class ContanctInSite(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    succes_url = reverse_lazy('home')
    
    
    def get_user_context(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



