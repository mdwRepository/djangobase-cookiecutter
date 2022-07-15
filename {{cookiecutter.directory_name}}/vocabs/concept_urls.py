from django.urls import path
from . import views
#from .sitemaps import SkosConceptSchemeSitemap

#sitemaps = {
#    'skosconceptschemes': SkosConceptSchemeSitemap,
#}

app_name = 'skosconcepts'

urlpatterns = [
    path('concepts/', views.SkosConceptListView.as_view(), name='browse_skosconcepts'),
    path('concepts/table/', views.SkosConceptTableListView.as_view(), name='list_skosconcepts'),
    path('concepts/<slug:slug>', views.SkosConceptDetailView.as_view(), name='skosconcept_detail'),
    path('concepts/create/', views.SkosConceptCreate.as_view(), name='skosconcept_create'),
    path('concepts/update/<int:pk>', views.SkosConceptUpdate.as_view(), name='skosconcept_update'),
    path('concepts/delete/<int:pk>', views.SkosConceptDelete.as_view(), name='skosconcept_delete'),
]