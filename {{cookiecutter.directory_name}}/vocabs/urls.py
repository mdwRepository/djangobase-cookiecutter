from django.urls import include, path

urlpatterns = [
    path('skos/', include('vocabs.scheme_urls', namespace='skosconceptschemes')),
    path('skos/', include('vocabs.concept_urls', namespace='skosconcepts')),
    path('skos/', include('vocabs.collection_urls', namespace='skoscollections')),
    path('skos/', include('vocabs.skos_urls', namespace='skos')),
    path('skos/', include('vocabs.dal_urls', namespace='skos-ac')),
]
