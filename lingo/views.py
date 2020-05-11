from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.utils.translation import LANGUAGE_SESSION_KEY, get_language_from_request
from django.views.generic import TemplateView
from lingo.meetings.models import Meeting


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        meetings = Meeting.objects.exclude(cancelled=True)
        context.update({
            'meeting_now':meetings.filter(time__lte=now, time__gt=now - timedelta(minutes=120)).first(),
            'meetings_soon': meetings.filter(time__gte=now).exclude(type=2).order_by('time')[:6],
            'meetings_community': meetings.filter(time__gte=now).filter(type=2).order_by('time')[:6],
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


def set_profile_language_middleware(get_response):
    def middleware(request):
        if not request.user.is_anonymous:
            profile = request.user.profile
            lang = get_language_from_request(request)
            if profile.profile_language != lang:
                profile.profile_language = lang
                profile.save()
        return get_response(request)

    return middleware
