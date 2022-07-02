from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('', include(('infos.info_urls', 'infos'), namespace='infos')),
]
