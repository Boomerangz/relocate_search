from django.db.models import Q
from django.views.generic import ListView

from relocate_search.models import Job, JobLocation


class JobsList(ListView):
    template_name = "jobs_list.html"
    model = Job
    ordering = ["location__name", "name"]

    def get_queryset(self, *args,**kwargs):
        queryset = super(JobsList, self).get_queryset(*args, **kwargs).filter(deleted=False)
        if self.request.GET.get('location_id'):
            queryset = queryset.filter(location__id=self.request.GET.get('location_id'))
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = queryset.filter(Q(name__icontains=search)|Q(tags__name__iexact=search.lower())|Q(location__name__icontains=search.lower()))
        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context = super(JobsList, self).get_context_data(**kwargs)
        context['locations_list'] = JobLocation.objects.order_by('name')
        return context

