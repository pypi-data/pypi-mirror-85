# noqa

from django.contrib import admin

from reversion.admin import VersionAdmin

from .mixins import BaseModelAdmin
from .models import (
    Activity,
    Announcement,
    AnnouncementRecipient,
    CustomMenuItem,
    Group,
    Notification,
    Person,
)

admin.site.register(Person, VersionAdmin)
admin.site.register(Group, VersionAdmin)
admin.site.register(Activity, VersionAdmin)
admin.site.register(Notification, VersionAdmin)
admin.site.register(CustomMenuItem, VersionAdmin)


class AnnouncementRecipientInline(admin.StackedInline):
    model = AnnouncementRecipient


class AnnouncementAdmin(BaseModelAdmin, VersionAdmin):
    inlines = [
        AnnouncementRecipientInline,
    ]


admin.site.register(Announcement, AnnouncementAdmin)
