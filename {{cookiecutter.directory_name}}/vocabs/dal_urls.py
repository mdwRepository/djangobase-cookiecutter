from django.urls import include, path
from . import dal_views
from .models import SkosConcept, SkosConceptScheme, SkosCollection
from django.conf import settings
from users.models import CustomGroup

app_name = 'vocabs'

urlpatterns = [
    path('autocomplete/external-link/', dal_views.ExternalLinkAC.as_view(), name='external-link-ac'),
    path('autocomplete/skosconceptscheme/', dal_views.SkosConceptSchemeAC.as_view(model=SkosConceptScheme),
         name='skosconceptscheme-autocomplete'),
    path('autocomplete/skoscollection/', dal_views.SkosCollectionAC.as_view(model=SkosCollection),
         name='skoscollection-autocomplete'),
    path('autocomplete/skosconcept/', dal_views.SkosConceptAC.as_view(model=SkosConcept),
         name='skosconcept-autocomplete'),
    path('autocomplete/skosconcept-extmatch/', dal_views.SkosConceptExternalMatchAC.as_view(model=SkosConcept),
         name='skosconcept-extmatch-autocomplete'),
    path('autocomplete/user/', dal_views.UserAC.as_view(model=settings.AUTH_USER_MODEL),
         name='user-autocomplete'),
    path('autocomplete/group/', dal_views.GroupAC.as_view(model=CustomGroup),
         name='group-autocomplete'),
]
