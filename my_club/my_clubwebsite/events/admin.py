from django.contrib import admin
from .models import Venue, Member, Event

# Register your models here.

# admin.site.register(Venue)
admin.site.register(Member)


# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)  # use -name for it to start from z-a
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date',)
