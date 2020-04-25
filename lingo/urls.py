from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.contrib.auth.views import LoginView
from lingo.meetings.views import meeting_list, meeting_detail, meeting_rsvp, meeting_rsvp_cancel, meeting_request
from lingo.views import IndexView, signup, set_language, AuthForm


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=AuthForm
    ), name='auth'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),

    path('lang/', set_language, name='set_lang'),

    path('', IndexView.as_view(), name='index'),

    path('meetings/<int:meeting_id>/', meeting_detail, name='meeting_detail'),
    path('meetings/<int:meeting_id>/rsvp/', meeting_rsvp, name='meeting_rsvp'),
    path('meetings/<int:meeting_id>/rsvp_cancel/', meeting_rsvp_cancel, name='meeting_rsvp_cancel'),
    path('meetings/request/', meeting_request, name='meeting_request'),
    path('meetings/', meeting_list, name='meeting_list'),

    path('docs/details/', TemplateView.as_view(template_name='docs/details.html'), name='docs_details'),
    path('docs/conducts/', TemplateView.as_view(template_name='docs/conduct.html'), name='docs_conduct'),
    path('docs/privacy/', TemplateView.as_view(template_name='docs/privacy.html'), name='docs_privacy'),
]


admin.site.index_title = _('Lingo Cafe')
admin.site.site_header = _('Lingo Cafe Administration')
admin.site.site_title = _('Lingo Cafe Management')
