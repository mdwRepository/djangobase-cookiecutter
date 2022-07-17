# -*- coding: UTF-8 -*-

from django.contrib.sitemaps import Sitemap
from guardian.shortcuts import get_objects_for_user

from .models import SkosConcept, SkosConceptScheme, SkosCollection
from users.models import CustomUser


class SkosConceptSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconcept'),
                                    klass=SkosConcept).all()

    def lastmod(self, obj):
        return obj.modified_at


class SkosConceptSchemeSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconceptscheme'),
                                    klass=SkosConceptScheme).all()

    def lastmod(self, obj):
        return obj.modified_at


class SkosCollectionSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skoscollection'),
                                    klass=SkosCollection).all()

    def lastmod(self, obj):
        return obj.modified_at
