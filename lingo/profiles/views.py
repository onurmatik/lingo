import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AuthForm(AuthenticationForm):
    class Meta:
        labels = {
            'username': _('Email address'),
        }


class SignUpForm(UserCreationForm):
    username = forms.EmailField(max_length=254, label=_('Email'))
    first_name = forms.CharField(max_length=30, label=_('Name'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']


def signup(request):
    if not request.user.is_anonymous:
        messages.warning(request, _('You are already logged in!'))
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.email = form.cleaned_data.get('username')
            u.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=u.username, password=raw_password)
            login(request, user)
            messages.success(request, _('Welcome to Lingo Cafe! A confirmation email is sent to %s.') % u.email)
            user.email_user(
                _('Welcome to Lingo Cafe!'),
                render_to_string('registration/email_confirmation.html', {
                    'user': user,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }),
            )
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.save()
        login(request, user)
        messages.success(request, _('Your email is confirmed successfully!'))
    else:
        messages.error(request, _(
            'Email confirmation failed!'
        ))
    return redirect('index')
