from datetime import timedelta
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django import forms
from lingo.meetings.models import Meeting
from lingo.profiles.models import Profile


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
            'meetings_soon': Meeting.objects.filter(time__gte=now).order_by('time')[:6],
            'now': now,
        })
        if not self.request.user.is_anonymous:
            qs = Meeting.objects.filter(time__gt=timezone.now() - timedelta(minutes=120))
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
