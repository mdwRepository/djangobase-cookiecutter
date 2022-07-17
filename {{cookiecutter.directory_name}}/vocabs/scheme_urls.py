from django.urls import path
from guardian.shortcuts import get_objects_for_user
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from users.models import CustomUser
from . import views
from .models import SkosConceptScheme
from .feed import LatestSkosConceptSchemeRssFeed, LatestSkosConceptSchemeAtomFeed

info_dict_conceptscheme = {'queryset': get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                                       ('view_skosconceptscheme'), klass=SkosConceptScheme).all()}

app_name = 'skosconceptschemes'

urlpatterns = [
    path('scheme/', views.SkosConceptSchemeListView.as_view(), name='browse_skosconceptschemes'),
    path('scheme/table/', views.SkosConceptSchemeTableListView.as_view(), name='list_skosconceptschemes'),
    path('scheme/<slug:slug>', views.SkosConceptSchemeDetailView.as_view(), name='skosconceptscheme_detail'),
    path('scheme/create/', views.SkosConceptSchemeCreate.as_view(), name='skosconceptscheme_create'),
    path('scheme/update/<int:pk>', views.SkosConceptSchemeUpdate.as_view(), name='skosconceptscheme_update'),
    path('scheme/delete/<int:pk>', views.SkosConceptSchemeDelete.as_view(), name='skosconceptscheme_delete'),
    # feeds
    path('concepts/feed/rss', LatestSkosConceptSchemeRssFeed(), name="skosconceptscheme_rss_feed"),
    path('concepts/feed/atom', LatestSkosConceptSchemeAtomFeed(), name="skosconceptscheme_atom_feed"),
    # sitemap
    path('concepts/sitemap_skosconceptscheme.xml', sitemap,
         {'sitemaps': {'skosconceptscheme': GenericSitemap(info_dict_conceptscheme, priority=0.6, changefreq='daily')}},
         name='django.contrib.sitemaps.views.sitemap'),
]
