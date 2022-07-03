from django.urls import include, path
from . import views
from .feed import *


app_name = 'vocabs'

urlpatterns = [
    path('concepts/', views.SkosConceptListView.as_view(), name="browse_vocabs"),
    path('concepts/table/', views.SkosConceptTableListView.as_view(), name='list_vocabs'),
    #path('concepts/<int:pk>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    path('concepts/<slug:slug>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    path('concepts/create/', views.SkosConceptCreate.as_view(), name='skosconcept_create'),
    path('concepts/update/<int:pk>', views.SkosConceptUpdate.as_view(), name='skosconcept_update'),
    path('concepts/delete/<int:pk>', views.SkosConceptDelete.as_view(), name='skosconcept_delete'),
    path('concepts/feed/rss', LatestSkosConceptRssFeed(), name="persons_rss_feed"),
    path('concepts/feed/atom', LatestSkosConceptAtomFeed(), name="persons_atom_feed"),

    path('scheme/', views.SkosConceptSchemeListView.as_view(), name='browse_schemes'),
    # path('scheme/<int:pk>', views.SkosConceptSchemeDetailView.as_view(), name='skosconceptscheme_detail'),
    path('scheme/<slug:slug>', views.SkosConceptSchemeDetailView.as_view(), name='skosconceptscheme_detail'),
    path('scheme/create/', views.SkosConceptSchemeCreate.as_view(), name='skosconceptscheme_create'),
    path('scheme/update/<int:pk>', views.SkosConceptSchemeUpdate.as_view(), name='skosconceptscheme_update'),
    path('scheme/delete/<int:pk>', views.SkosConceptSchemeDelete.as_view(), name='skosconceptscheme_delete'),
    path('vocabs-download/', views.SkosConceptDL.as_view(), name='vocabs-download'),
    path('collection/', views.SkosCollectionListView.as_view(), name='browse_skoscollections'),
    #path('collection/<int:pk>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    path('collection/<slug:slug>', views.SkosCollectionDetailView.as_view(), name='skoscollection_detail'),
    path('collection/create/', views.SkosCollectionCreate.as_view(), name='skoscollection_create'),
    path('collection/update/<int:pk>', views.SkosCollectionUpdate.as_view(), name='skoscollection_update'),
    path('collection/delete/<int:pk>', views.SkosCollectionDelete.as_view(), name='skoscollection_delete'),
    path('import/', views.file_upload, name='import'),
]
