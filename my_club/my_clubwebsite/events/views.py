from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponse
import csv

# import Pagination Stuff
from django.core.paginator import Paginator


# Create your views here.

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment ; filename=venues.csv'

    # create a writer
    writer = csv.writer(response)

    # designate the model
    venues = Venue.objects.all()

    # add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'zip Code', 'phone', 'Web Address', 'Email Address'])
    # loop through and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.website, venue.email_address])
    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment ; filename=venues.txt'
    # designate the model
    venues = Venue.objects.all()

    # create blank list
    lines = []
    # loop through and output
    for venue in venues:
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.website}\n{venue.email_address}\n\n\n')
    # lines = ['This is line 1 \n',
    # 'this is line 2 \n',
    # 'This is line 3\n']

    # write to TextFile
    response.writelines(lines)
    return response


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')


def add_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted
    }
    return render(request, 'events/add_event.html', context)


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    context = {
        'event': event,
        'form': form
    }
    return render(request, 'events/update_event.html', context)


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    context = {
        'venue': venue,
        'form': form
    }
    return render(request, 'events/update_venue.html', context)


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        context = {
            'searched': searched,
            'venues': venues
        }
        return render(request, 'events/search_venue.html', context)
    else:
        context = {
        }
        return render(request, 'events/search_venue.html', context)


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    context = {
        'venue': venue
    }
    return render(request, 'events/show_venue.html', context)


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')

    # set up pagination
    p = Paginator(Venue.objects.all(), 1)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    context = {
        'venue_list': venue_list,
        'venues':venues,
        'nums':nums
    }
    return render(request, 'events/venues.html', context)


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted
    }
    return render(request, 'events/add_venue.html', context)


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    context = {
        'event_list': event_list
    }
    return render(request, 'events/event_list.html', context)


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Ben"
    # convert month from calender
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calender
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )

    # get current year
    now = datetime.now()
    current_year = now.year

    # get current time
    time = now.strftime('%I:%M:%S %p')

    context = {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    }
    return render(request, 'events/home.html', context)
