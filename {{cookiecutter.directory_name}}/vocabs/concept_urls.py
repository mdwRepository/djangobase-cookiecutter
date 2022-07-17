from django.urls import path
from guardian.shortcuts import get_objects_for_user
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from users.models import CustomUser
from . import views
from .models import SkosConcept
from .feed import LatestSkosConceptRssFeed, LatestSkosConceptAtomFeed

info_dict_concept = {'queryset': get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                                       ('view_skosconcept'), klass=SkosConcept).all()}

app_name = 'skosconcepts'

urlpatterns = [
    path('concepts/', views.SkosConceptListView.as_view(), name='browse_skosconcepts'),
    path('concepts/table/', views.SkosConceptTableListView.as_view(), name='list_skosconcepts'),
    path('concepts/<slug:slug>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    path('concepts/create/', views.SkosConceptCreate.as_view(), name='skosconcept_create'),
    path('concepts/update/<int:pk>', views.SkosConceptUpdate.as_view(), name='skosconcept_update'),
    path('concepts/delete/<int:pk>', views.SkosConceptDelete.as_view(), name='skosconcept_delete'),
    # feeds
    path('concepts/feed/rss', LatestSkosConceptRssFeed(), name="skosconcept_rss_feed"),
    path('concepts/feed/atom', LatestSkosConceptAtomFeed(), name="skosconcept_atom_feed"),
    # sitemap
    path('concepts/sitemap_skosconcept.xml', sitemap,
         {'sitemaps': {'skosconcept': GenericSitemap(info_dict_concept, priority=0.6, changefreq='daily')}},
         name='django.contrib.sitemaps.views.sitemap'),
]
