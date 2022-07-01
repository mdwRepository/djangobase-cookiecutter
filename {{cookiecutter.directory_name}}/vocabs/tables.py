import django_tables2 as tables
from django_tables2.utils import A
from vocabs.models import *


class SkosConceptSchemeTable(tables.Table):
    title = tables.LinkColumn('vocabs:skosconceptscheme_detail', args=[A('slug')])

    class Meta:
        model = SkosConceptScheme
        sequence = ['id', 'title', 'slug']
        attrs = {"class": "table table-hover table-striped table-condensed"}


class SkosCollectionTable(tables.Table):
    name = tables.LinkColumn('vocabs:skoscollection_detail', args=[A('slug')])

    class Meta:
        model = SkosCollection
        sequence = ['id', 'name', 'scheme', 'slug']
        attrs = {"class": "table table-hover table-striped table-condensed"}


class SkosConceptTable(tables.Table):
    pref_label = tables.LinkColumn('vocabs:skosconcept_detail', args=[A('slug')])

    class Meta:
        model = SkosConcept
        sequence = ['id', 'pref_label', 'slug']
        attrs = {"class": "table table-hover table-striped table-condensed"}
