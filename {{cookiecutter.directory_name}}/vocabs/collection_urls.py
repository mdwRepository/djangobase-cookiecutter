from django.urls import path
from . import views
#from .sitemaps import SkosConceptSchemeSitemap

#sitemaps = {
#    'skosconceptschemes': SkosConceptSchemeSitemap,
#}

app_name = 'skoscollections'

urlpatterns = [
    path('collections/', views.SkosCollectionListView.as_view(), name='browse_skoscollections'),
    path('collections/table/', views.SkosCollectionTableListView.as_view(), name='list_skoscollections'),
    path('collections/<slug:slug>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    path('collections/create/', views.SkosCollectionCreate.as_view(), name='skoscollection_create'),
    path('collections/update/<int:pk>', views.SkosCollectionUpdate.as_view(), name='skoscollection_update'),
    path('collections/delete/<int:pk>', views.SkosCollectionDelete.as_view(), name='skoscollection_delete'),
]