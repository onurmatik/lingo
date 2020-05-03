from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from lingo.languages.models import Language


LEVELS = (
    ('A', _(
        'I can catch some words in texts or speeches. '
        'From time to time, by combining these words, I can grasp the context and the general meaning, '
        'but I cannot get a complete idea of the content of the text / speech; '
        'I have a hard time speaking / I cannot speak.'
    )),
    ('B', _(
        'When I read simple texts, I can get a rough idea of the general subject; '
        'I can understand the main idea of slow and clear conversations; '
        'I cannot understand complex texts or speeches; '
        'I have difficulty speaking / I cannot speak.'
    )),
    ('C', _(
        'I can understand texts / speeches mostly unless they are complex, '
        'but I want to grasp more and master the whole. '
        'I can speak slowly with a limited vocabulary, '
        'I want to be fluent, improve my vocabulary.'
    ))
)


class Meeting(models.Model):
    language = models.ForeignKey(Language, verbose_name=_('language'), on_delete=models.CASCADE)
    time = models.DateTimeField(_('time'))
    notes = models.TextField(blank=True, null=True)
    resources = models.ManyToManyField('Resource', through='MeetingResource', verbose_name=_('meeting resource'))
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


class Resource(models.Model):
    title = models.CharField(_('title'), max_length=50)
    url = models.URLField(_('URL'), blank=True, null=True)
    type = models.CharField(_('resource type'), max_length=1, choices=(
        ('r', 'reading'),
        ('l', 'listening'),
        ('w', 'watching'),
    ))
    description = models.TextField(_('description'), blank=True, null=True)
    language = models.ForeignKey(Language, verbose_name=_('language'), on_delete=models.CASCADE)
    level = models.CharField(_('level'), max_length=1, choices=LEVELS, blank=True, null=True)

    def __str__(self):
        return self.title


class MeetingResource(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name=_('resource'))
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, verbose_name=_('meeting'))
    time = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)


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
