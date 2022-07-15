from django.urls import path
from . import views
#from .sitemaps import SkosConceptSchemeSitemap

#sitemaps = {
#    'skosconceptschemes': SkosConceptSchemeSitemap,
#}

app_name = 'skosconceptschemes'

urlpatterns = [
    path('scheme/', views.SkosConceptSchemeListView.as_view(), name='browse_skosconceptschemes'),
    path('scheme/table/', views.SkosConceptSchemeTableListView.as_view(), name='list_skosconceptschemes'),
    path('scheme/<slug:slug>', views.SkosConceptSchemeDetailView.as_view(), name='skosconceptscheme_detail'),
    path('scheme/create/', views.SkosConceptSchemeCreate.as_view(), name='skosconceptscheme_create'),
    path('scheme/update/<int:pk>', views.SkosConceptSchemeUpdate.as_view(), name='skosconceptscheme_update'),
    path('scheme/delete/<int:pk>', views.SkosConceptSchemeDelete.as_view(), name='skosconceptscheme_delete'),
]