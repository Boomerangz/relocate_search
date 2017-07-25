from django.views.generic import ListView

from relocate_search.models import JobLocation


class LocationsList(ListView):
    model = JobLocation
    template_name = 'locations_list.html'