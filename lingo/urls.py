from django.contrib import admin
from django.urls import path, include
from lingo.meetings.views import meeting_list, meeting_detail, meeting_rsvp_cancel, meeting_request
from lingo.views import IndexView, signup, set_language


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),

    path('', IndexView.as_view(), name='index'),

    path('meetings/<int:meeting_id>/', meeting_detail, name='meeting_detail'),
    path('meetings/<int:meeting_id>/meeting_rsvp_cancel/', meeting_rsvp_cancel, name='meeting_rsvp_cancel'),
    path('meetings/request/', meeting_request, name='meeting_request'),
    path('meetings/', meeting_list, name='meeting_list'),

    path('lang/', set_language, name='set_lang'),

]
