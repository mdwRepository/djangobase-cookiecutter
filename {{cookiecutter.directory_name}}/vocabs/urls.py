from django.conf.urls import url
from django.urls import include, path
from . import views
from .feed import *
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from guardian.shortcuts import get_objects_for_user

from users.models import CustomUser

info_dict_skosconcept = {'queryset': get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                                          ('view_skosconcept'), klass=SkosConcept).all()}

urlpatterns = [
    # add django view urlpatterns
    path('skos/', include('vocabs.scheme_urls', namespace='skosconceptschemes')),
    path('skos/', include('vocabs.concept_urls', namespace='skosconcepts')),
    path('skos/', include('vocabs.collection_urls', namespace='skoscollections')),
    path('skos/', include('vocabs.skos_urls', namespace='skos')),
    path('skos/', include('vocabs.dal_urls', namespace='skos-ac')),

    #path('concepts/', views.SkosConceptListView.as_view(), name="browse_vocabs"),
    #path('concepts/table/', views.SkosConceptTableListView.as_view(), name='list_vocabs'),
    # path('concepts/<int:pk>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    #path('concepts/<slug:slug>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    #path('concepts/create/', views.SkosConceptCreate.as_view(), name='skosconcept_create'),
    #path('concepts/update/<int:pk>', views.SkosConceptUpdate.as_view(), name='skosconcept_update'),
    #path('concepts/delete/<int:pk>', views.SkosConceptDelete.as_view(), name='skosconcept_delete'),

    # feeds
    #path('concepts/feed/rss', LatestSkosConceptRssFeed(), name="persons_rss_feed"),
    #path('concepts/feed/atom', LatestSkosConceptAtomFeed(), name="persons_atom_feed"),

    # add sitemaps urlpatterns for search engines
    #path('sitemap_skosconcept.xml', sitemap,
    #     {'sitemaps': {'concept': GenericSitemap(info_dict_skosconcept, priority=0.6, changefreq='daily')}},
    #     name='django.contrib.sitemaps.views.sitemap'),

    #path('collection/', views.SkosCollectionListView.as_view(), name='browse_skoscollections'),
    #path('collection/table/', views.SkosCollectionTableListView.as_view(), name='list_skoscollections'),
    # path('collection/<int:pk>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    #path('collection/<slug:slug>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    #path('collection/create/', views.SkosCollectionCreate.as_view(), name='skoscollection_create'),
    #path('collection/update/<int:pk>', views.SkosCollectionUpdate.as_view(), name='skoscollection_update'),
    #path('collection/delete/<int:pk>', views.SkosCollectionDelete.as_view(), name='skoscollection_delete'),

]
