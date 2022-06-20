"""djangobaseproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import traceback

from importlib import import_module
from sys import stdout

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webpage.urls', namespace='webpage')),
    path('infos/', include('infos.urls', namespace='infos')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# import urls from LOCAL_APPS as defines in base.py
for app in settings.LOCAL_APPS:
    try:
        # get urls.py from the respective app
        print(f"############## {app} ##############")
        _module = import_module('%s.urls' % app)
        if settings.DEBUG:
            print(app)
        urlpatterns += _module.urlpatterns
    except Exception as error:
        stdout.write(f"Error: {error}, {traceback.format_exc()}")

handler404 = 'webpage.views.handler404'

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.urls import get_resolver

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

    print(get_resolver().url_patterns)
