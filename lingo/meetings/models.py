from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from lingo.languages.models import Language


class Meeting(models.Model):
    language = models.ForeignKey(Language, verbose_name=_('language'), on_delete=models.CASCADE)
    time = models.DateTimeField(_('time'))
    password = models.CharField(_('Meeting password'), max_length=20, blank=True, null=True)
    host = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='hosted_meetings',
        verbose_name=_('meeting host'),
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        through='MeetingParticipant',
        related_name='participated_meetings',
        verbose_name=_('participants'),
    )
    start_url = models.URLField(_('Start URL'), blank=True, null=True)
    join_url = models.URLField(_('Join URL'), blank=True, null=True)

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


class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('participant'))
    tutor = models.BooleanField(_('tutor'), default=False)
    joined = models.DateTimeField(_('time joined'), auto_now_add=True)

    class Meta:
        unique_together = (('meeting', 'participant'),)


class MeetingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_('language'))
    tutor = models.BooleanField(_('tutor'), default=False, choices=(
        (False, _('Practice')),
        (True, _('Tutor')),
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