from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from lingo.meetings.models import Meeting


class AuthForm(AuthenticationForm):
    class Meta:
        labels = {
            'username': _('Email address'),
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label=_('Name'))
    username = forms.EmailField(max_length=254, label=_('Email'))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2',)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.email = form.cleaned_data.get('username')
            u.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=u.username, password=raw_password)
            login(request, user)
            messages.success(request, _('Welcome to Lingo Cafe!'))
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context.update({
            'meeting_now': Meeting.objects.filter(time__lte=now, time__gt=now - timedelta(minutes=120)).first(),
            'meetings_soon': Meeting.objects.filter(time__gte=now).exclude(type=2).order_by('time')[:6],
            'meetings_community': Meeting.objects.filter(time__gte=now).filter(type=2).order_by('time')[:6],
            'now': now,
        })
        if not self.request.user.is_anonymous:
            qs = Meeting.objects.filter(time__gt=timezone.now() - timedelta(minutes=120)).exclude(type=2)
            context.update({
                'meetings_user': qs.filter(
                    participants=self.request.user
                ).distinct().order_by('time'),
                'meetings_suggested': qs.filter(
                    language__in=self.request.user.profile.languages.all()
                ).exclude(
                    participants=self.request.user
                ).order_by('time'),
            })
        return context


def set_language(request):
    next_page = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(next_page) if next_page else HttpResponseRedirect('/')
    lang_code = request.GET.get('lang')
    next_trans = translate_url(next_page, lang_code)
    if next_trans != next_page:
        response = HttpResponseRedirect(next_trans)
    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = lang_code
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
    )
    return response
