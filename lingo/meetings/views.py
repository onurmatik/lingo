from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import forms
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from lingo.profiles.models import ProfileLanguage
from .models import Meeting, MeetingParticipant, MeetingRequest


def meeting_list(request):
    now = timezone.now()
    return render(request, 'index.html', {
        'now': Meeting.objects.filter(time__lte=now, time__gt=now+timedelta(minutes=60)),
        'soon': Meeting.objects.filter(time__gte=now)[:5],
    })


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    context = {
        'meeting': meeting,
    }
    if not request.user.is_anonymous:
        participation = MeetingParticipant.objects.filter(
            meeting=meeting,
            participant=request.user,
        ).first()
        context.update({
            'participation': participation
        })
        if not participation:
            context.update({
                'form': RsvpForm()
            })
    return render(request, 'meetings/meeting_detail.html', context)


class RsvpForm(forms.Form):
    tutor = forms.ChoiceField(
        choices=(
            (False, _('I want to practice')),
            (True, _('I want to tutor')),
        ),
        widget=forms.RadioSelect(),
        initial=False,
    )


@login_required
def meeting_rsvp(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            MeetingParticipant.objects.update_or_create(
                meeting=meeting,
                participant=request.user,
                defaults={
                    'tutor': form.cleaned_data['tutor'],
                }
            )
            ProfileLanguage.objects.update_or_create(
                profile=request.user.profile,
                language=meeting.language,
                defaults={
                    'tutor': form.cleaned_data['tutor'],
                }
            )
            return redirect('meeting_detail', meeting_id=meeting.id)
    else:
        form = RsvpForm()
    return render(request, 'meetings/rsvp_form.html', {
        'meeting': meeting,
        'form': form,
    })



@login_required
def meeting_rsvp_cancel(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    MeetingParticipant.objects.filter(
        meeting=meeting,
        participant=request.user,
    ).delete()
    return redirect('index')


class MeetingRequestForm(forms.ModelForm):
    class Meta:
        model = MeetingRequest
        fields = ['language', 'tutor', 'country', 'notes']
        labels = {
            'tutor': _('Your role'),
            'country': _('Your country'),
        }
        help_texts = {
            'language': _('Language of the session you are suggesting.'),
            'tutor': _('You can participate in a session to practice or to tutor the language.'),
            'country': _('The country you are living in.'),
            'notes': _('Specify if you have anything to add.'),
        }
        widgets = {
            'tutor': forms.RadioSelect(),
            'language': forms.Select(attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
            }),
            'country': forms.Select(attrs={
                'class': 'selectpicker',
                'data-live-search': 'true',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
            }),
        }


@login_required
def meeting_request(request):
    if request.method == 'POST':
        form = MeetingRequestForm(request.POST)
        if form.is_valid():
            mr = form.save(commit=False)
            mr.user = request.user
            mr.save()
            messages.success(request, _('Thank you! Your sugestion is recorded.'))
            ProfileLanguage.objects.get_or_create(
                profile=request.user.profile,
                language=mr.language,
                tutor=mr.tutor,
            )
            if mr.country:
                profile = request.user.profile
                if not profile.country:
                    profile.country = mr.country
                    profile.save()
            return redirect('index')
    else:
        form = MeetingRequestForm()
    return render(request, 'meetings/request_form.html', {
        'form': form,
    })
