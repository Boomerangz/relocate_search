from django.db.models import Q
from django.views.generic import ListView

from relocate_search.models import JobLocation, Job


class LocationsList(ListView):
    model = JobLocation
    template_name = 'locations_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(LocationsList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            jobs = Job.objects.filter(Q(name__icontains=search)|Q(tags__name__iexact=search.lower())).filter(deleted=False)
            job_locations = set(jobs.values_list('location_id', flat=True))
            queryset = queryset.filter(pk__in=job_locations)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(LocationsList, self).get_context_data(*args, **kwargs)
        search = self.request.GET.get('search')
        for i in context['object_list']:
            i.jobs_count = Job.objects.filter(location_id=i.id).filter(Q(name__icontains=search)|Q(tags__name__iexact=search.lower())).filter(deleted=False).distinct().count()
        return context