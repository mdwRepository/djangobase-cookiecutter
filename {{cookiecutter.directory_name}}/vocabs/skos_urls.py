from django.urls import path
from . import views
#from .sitemaps import SkosConceptSchemeSitemap

#sitemaps = {
#    'skosconceptschemes': SkosConceptSchemeSitemap,
#}

app_name = 'skos'

urlpatterns = [
    path('download/', views.SkosConceptDL.as_view(), name='vocabs-download'),
    path('import/', views.file_upload, name='import'),
]