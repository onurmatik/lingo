from django.contrib import admin
from .models import Meeting, MeetingParticipant, MeetingRequest, MeetingPoll


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['language', 'host', 'time', 'start_url', 'join_url']
    list_filter = ['language', 'time']
    search_fields = ['host__username']
    autocomplete_fields = ['language', 'host', 'participants']


@admin.register(MeetingParticipant)
class MeetingParticipantAdmin(admin.ModelAdmin):
    list_display = ['participant', 'meeting', 'meeting_time', 'tutor', 'joined']
    autocomplete_fields = ['meeting', 'participant']

    def meeting_time(self, obj):
        return obj.meeting.time
    meeting_time.admin_order_field = 'meeting__time'


@admin.register(MeetingRequest)
class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'tutor', 'country', 'time']


@admin.register(MeetingPoll)
class MeetingFeedbackAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user', 'rate', 'notes', 'time']
