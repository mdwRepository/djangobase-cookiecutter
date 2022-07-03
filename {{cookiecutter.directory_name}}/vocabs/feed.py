# -*- coding: UTF-8 -*-

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from .models import SkosConcept


class LatestSkosConceptRssFeed(Feed):

    title = _('SKOS Concept RSS 2.0 Feed')
    link = reverse_lazy('vocabs:browse_vocabs')
    description = _('New SKOS Concept feed.')

    def items(self):
        return SkosConcept.objects.all()[:15]

    def item_title(self, item):
        return item.pref_label


class LatestSkosConceptAtomFeed(Feed):

    title = _('SKOS Concept Atom Feed')
    link = reverse_lazy('vocabs:browse_vocabs')
    description = _('New SKOS Concept feed.')
    feed_type = Atom1Feed

    def items(self):
        return SkosConcept.objects.all()[:15]

    def item_title(self, item):
        return item.pref_label
