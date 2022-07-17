# -*- coding: UTF-8 -*-

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import get_objects_for_user

from .models import SkosConcept, SkosConceptScheme, SkosCollection
from users.models import CustomUser


class LatestSkosConceptRssFeed(Feed):

    title = _('SKOS Concept RSS 2.0 Feed')
    link = reverse_lazy('skosconcepts:browse_skosconcepts')
    description = _('New SKOS Concept feed.')

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconcept'),
                                    klass=SkosConcept).all()[:15]

    def item_title(self, item):
        return item.pref_label


class LatestSkosConceptAtomFeed(Feed):

    title = _('SKOS Concept Atom Feed')
    link = reverse_lazy('skosconcepts:browse_skosconcepts')
    description = _('New SKOS Concept feed.')
    feed_type = Atom1Feed

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconcept'),
                                    klass=SkosConcept).all()[:15]

    def item_title(self, item):
        return item.pref_label


class LatestSkosConceptSchemeRssFeed(Feed):

    title = _('SKOS Concept Scheme RSS 2.0 Feed')
    link = reverse_lazy('skosconceptschemes:browse_skosconceptschemes')
    description = _('New SKOS Concept Scheme feed.')

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconceptscheme'),
                                    klass=SkosConceptScheme).all()[:15]

    def item_title(self, item):
        return item.title


class LatestSkosConceptSchemeAtomFeed(Feed):

    title = _('SKOS Concept Scheme Atom Feed')
    link = reverse_lazy('skosconceptschemes:browse_skosconceptschemes')
    description = _('New SKOS Concept Scheme feed.')
    feed_type = Atom1Feed

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skosconceptscheme'),
                                    klass=SkosConceptScheme).all()[:15]

    def item_title(self, item):
        return item.title


class LatestSkosCollectionRssFeed(Feed):

    title = _('SKOS Collections RSS 2.0 Feed')
    link = reverse_lazy('skoscollections:browse_skosconceptschemes')
    description = _('New SKOS Collections feed.')

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skoscollection'),
                                    klass=SkosCollection).all()[:15]

    def item_title(self, item):
        return item.title


class LatestSkosCollectionAtomFeed(Feed):

    title = _('SKOS Collection Atom Feed')
    link = reverse_lazy('skoscollections:browse_skoscollections')
    description = _('New SKOS Collections feed.')
    feed_type = Atom1Feed

    def items(self):
        return get_objects_for_user(CustomUser.objects.get(username='AnonymousUser'),
                                    ('view_skoscollection'),
                                    klass=SkosCollection).all()[:15]

    def item_title(self, item):
        return item.title
