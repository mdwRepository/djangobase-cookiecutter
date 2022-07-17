from django.urls import path
from guardian.shortcuts import get_objects_for_user
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from users.models import CustomUser
from . import views
from .models import SkosCollection
from .feed import LatestSkosCollectionsRssFeed, LatestSkosCollectionsAtomFeed

info_dict_collection = {'queryset': get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                                       ('view_skoscollection'), klass=SkosCollection).all()}

app_name = 'skoscollections'

urlpatterns = [
    path('collections/', views.SkosCollectionListView.as_view(), name='browse_skoscollections'),
    path('collections/table/', views.SkosCollectionTableListView.as_view(), name='list_skoscollections'),
    path('collections/<slug:slug>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    path('collections/create/', views.SkosCollectionCreate.as_view(), name='skoscollection_create'),
    path('collections/update/<int:pk>', views.SkosCollectionUpdate.as_view(), name='skoscollection_update'),
    path('collections/delete/<int:pk>', views.SkosCollectionDelete.as_view(), name='skoscollection_delete'),
    # feeds
    path('concepts/feed/rss', LatestSkosCollectionsRssFeed(), name="skoscollection_rss_feed"),
    path('concepts/feed/atom', LatestSkosCollectionsAtomFeed(), name="skoscollection_atom_feed"),
    # sitemap
    path('concepts/sitemap_skoscollection.xml', sitemap,
         {'sitemaps': {'skoscollection': GenericSitemap(info_dict_collection, priority=0.6, changefreq='daily')}},
         name='django.contrib.sitemaps.views.sitemap'),
]
