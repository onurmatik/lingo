from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from lingo.languages.models import Language


class Meeting(models.Model):
    language = models.ForeignKey(Language, verbose_name=_('language'), on_delete=models.CASCADE)
    time = models.DateTimeField(_('time'))
    host = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='hosted_meetings',
        verbose_name=_('meeting host'),
    )
    start_url = models.URLField(_('Start URL'), blank=True, null=True)
    join_url = models.URLField(_('Join URL'), blank=True, null=True)
    password = models.CharField(_('meeting password'), max_length=20, blank=True, null=True)
    participants = models.ManyToManyField(
        User,
        blank=True,
        through='MeetingParticipant',
        related_name='participated_meetings',
        verbose_name=_('participants'),
    )
    type = models.PositiveSmallIntegerField(_('meeting type'), choices=(
        (1, _('practice')),
        (2, _('community meeting')),
    ), default=1)
    cancelled = models.BooleanField(default=False)
    cancellation_reason = models.PositiveSmallIntegerField(blank=True, null=True, choices=(
        (1, _('no host')),
        (2, _('no participant')),
        (0, _('other')),
    ))

    def __str__(self):
        return str(_(self.language.name))

    def get_absolute_url(self):
        return reverse('meeting_detail', kwargs={
            'meeting_id': self.id
        })

    def save(self, **kwargs):
        if not self.start_url:
            # TODO: Zoom API things
            pass
        super().save(**kwargs)

    def clean(self):
        # TODO: check for overlaps
        pass


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('participant'))
    tutor = models.BooleanField(_('co-host'), default=False)
    joined = models.DateTimeField(_('time joined'), auto_now_add=True)

    class Meta:
        unique_together = (('meeting', 'participant'),)


class MeetingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_('language'))
    tutor = models.BooleanField(_('co-host'), default=False, choices=(
        (False, _('participant')),
        (True, _('co-host')),
    ))
    country = CountryField(_('country'), blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)


class MeetingPoll(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    rate = models.PositiveSmallIntegerField(_('rate'), choices=(
        (1, _('Poor')),
        (2, _('OK')),
        (3, _('Good')),
    ))
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)
