from django.db import models

from django.utils.translation import gettext_lazy as _

from .mixins import *


class Entity(models.Model):
    """
    "concrete or abstract thing that exists, did exist, or might exist, including associations
    among those things" (ISO 23081-1:2017(en), 3.7. Information and documentation — Records
    management processes — Metadata for records — Part 1: Principles)
    """

    class Meta:
        abstract = True
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")


class NamedEntity(Entity, BaseEntityMetadataMixin, ExtIdMixin, LifecycleMixin):
    """
    A databased entity, concept or class. This is a generic class that is the root
    of all the other classes.
    """

    class Meta:
        abstract = True
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")

