from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from lingo.languages.models import Language


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    country = CountryField(_('country'), blank=True, null=True)
    timezone = TimeZoneField(_('timezone'), blank=True, null=True)
    languages = models.ManyToManyField(
        Language,
        through='ProfileLanguage',
        blank=True,
        verbose_name=_('language')
    )

    def __str__(self):
        return self.user.username


class ProfileLanguage(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name=_('profile')
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name=_('language')
    )
    tutor = models.BooleanField(_('tutor'), default=False)
    time = models.DateTimeField(_('time'), auto_now_add=True)

    def __str__(self):
        return str(_(self.language.name))

    class Meta:
        unique_together = (('profile', 'language'),)


class Report(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_set',
        verbose_name=_('reported by')
    )
    notes = models.TextField(_('notes'), blank=True, null=True)
    time = models.DateTimeField(_('time'), auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(
        user=instance,
    )
models.signals.post_save.connect(create_profile, sender=User)
