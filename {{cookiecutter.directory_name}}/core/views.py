from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from guardian.shortcuts import get_objects_for_user
from reversion.models import Version


class BaseDetailView(DetailView):

    def get_queryset(self, **kwargs):
        qs = get_objects_for_user(self.request.user,
                                  perms=[
                                      'view_{}'.format(self.model.__name__.lower()),
                                      'change_{}'.format(self.model.__name__.lower()),
                                      'delete_{}'.format(self.model.__name__.lower()),
                                  ],
                                  klass=self.model)
        return qs

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)
        context['history'] = Version.objects.get_for_object(self.object)
        return context


class BaseDeleteView(DeleteView):

    def get_queryset(self, **kwargs):
        qs = get_objects_for_user(self.request.user,
                                  perms=[
                                      'view_{}'.format(self.model.__name__.lower()),
                                      'change_{}'.format(self.model.__name__.lower()),
                                      'delete_{}'.format(self.model.__name__.lower()),
                                  ],
                                  klass=self.model)
        return qs
