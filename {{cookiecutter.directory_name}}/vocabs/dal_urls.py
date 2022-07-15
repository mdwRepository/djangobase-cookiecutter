from django.urls import include, path
from . import dal_views
from .models import SkosConcept, SkosConceptScheme, SkosCollection
from django.conf import settings

from users.models import CustomGroup


app_name = 'vocabs'

urlpatterns = [
    path('external-link-ac/', dal_views.ExternalLinkAC.as_view(), name='external-link-ac'),
    path('skosconceptscheme-autocomplete/', dal_views.SkosConceptSchemeAC.as_view(model=SkosConceptScheme),
         name='skosconceptscheme-autocomplete'),
    path('skoscollection-autocomplete/', dal_views.SkosCollectionAC.as_view(model=SkosCollection),
         name='skoscollection-autocomplete'),
    path('skosconcept-autocomplete/', dal_views.SkosConceptAC.as_view(model=SkosConcept),
         name='skosconcept-autocomplete'),
    path('skosconcept-extmatch-autocomplete/', dal_views.SkosConceptExternalMatchAC.as_view(model=SkosConcept),
         name='skosconcept-extmatch-autocomplete'),
    path('user-autocomplete/', dal_views.UserAC.as_view(model=settings.AUTH_USER_MODEL),
         name='user-autocomplete'),
    path('group-autocomplete/', dal_views.GroupAC.as_view(model=CustomGroup),
         name='group-autocomplete'),
]
