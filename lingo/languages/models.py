from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class LanguageManager(models.Manager):
    def load(self):
        for code, name in settings.LANGUAGES:
            self.get_or_create(
                code=code,
                name=name,
            )


class Language(models.Model):
    code = models.CharField(_('code'), max_length=10)
    name = models.CharField(_('name'), max_length=20)

    objects = LanguageManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
