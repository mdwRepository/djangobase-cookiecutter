# -*- coding: UTF-8 -*-

import datetime
import logging
import uuid

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition, can_proceed

from .fields import CustomSmallTextField

logging.basicConfig(format='%(name)s-%(levelname)s-%(asctime)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------#
# Functions                                                                  #
# ---------------------------------------------------------------------------#

def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


# ---------------------------------------------------------------------------#
# Mixins                                                                     #
# ---------------------------------------------------------------------------#

# UNIQUE ID - UUID
# ----------------------------------------------------------------------------

class ExtIdMixin(models.Model):
    """
        External id (UUID4) mixin for a resource (can be referenced by other
        systems.
    """

    ext_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    ).set_extra(
        is_public=True,
    )

    class Meta:
        abstract = True

    @property
    def get_uuid(self):
        return str(self.ext_id)

    @staticmethod
    def uuid_to_hex(uth):
        return uuid.UUID(uth).hex

    @property
    def clean_uuid(self):
        return str(self.uuid_to_hex(self.ext_id))

    @classmethod
    def get_natural_primary_key(self):
        return str(self.ext_id)


# BASE ENTITY METADATA
# ----------------------------------------------------------------------------

class BaseEntityMetadataMixin(models.Model):
    title = models.CharField(
        # alternatively called name
        # limit to 255 chars for exports with other systems
        _("title"),
        max_length=255,
        help_text=_("The title of the resource."),
    ).set_extra(
        is_public=True,
    )
    description = CustomSmallTextField(
        # max. 2048 chars
        _("description"),
        null=True,
        blank=True,
        help_text=_("A basic description of the resource."),
    ).set_extra(
        is_public=True,
    )
    # dates & users
    created_at_time = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        null=True,
    ).set_extra(
        is_public=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_creator',
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("creator_help"),
    ).set_extra(
        is_public=True,
    )
    modified_at_time = models.DateTimeField(
        _("modified at"),
        auto_now=True,
        null=True,
    ).set_extra(
        is_public=True,
    )
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_modifier',
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("modifier_help"),
    ).set_extra(
        is_public=True,
    )
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='%(class)s' + '_contributor',
        help_text=_("contributors_help"),
    )
    # versioning
    current_major_version = models.IntegerField(
        editable=False,
        default=0,
        verbose_name=_('major_version')
    ).set_extra(
        is_public=True,
    )
    current_minor_version = models.IntegerField(
        editable=False,
        default=0,
        verbose_name=_('minor_version')
    ).set_extra(
        is_public=True,
    )
    current_revision_number = models.IntegerField(
        editable=False,
        default=0,
        verbose_name=_('revision number')
    ).set_extra(
        is_public=True,
    )
    # additional optional fields
    slug = models.SlugField(
        null=True,
        blank=True
    ).set_extra(
        is_public=True,
    )

    class Meta:
        abstract = True
        ordering = [
            'title',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


# LIFECYCLE
# ----------------------------------------------------------------------------

class LifecycleMixin(models.Model):
    """
        Lifecycle based on Finite State Machine
    """

    draft = 'draft'
    submitted = 'submitted'
    approved = 'approved'
    deleted = 'deleted'

    LIFECYCLE_STATES = (
        (draft, _('draft')),
        (submitted, _('submitted')),
        (approved, _('approved')),
        (deleted, _('deleted')),
    )

    status = FSMField(
        verbose_name=_('State'),
        max_length=36,
        help_text=_("mdwRepository lifecycle state"),
        choices=LIFECYCLE_STATES,
        default='draft',
    )
    first_published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    # FSM transitions

    @transition(field=status, source=draft, target=submitted)
    def submit(self):
        pass

    @transition(field=status, source=submitted, target=approved)
    def approve(self):
        pass

    @transition(field=status, source=[draft, submitted, approved], target=deleted)
    def delete(self):
        pass

    # FSM states

    @property
    def in_draft_state(self):
        return can_proceed(self.draft)

    @property
    def in_submitted_state(self):
        return can_proceed(self.submitted)

    @property
    def in_approved_state(self):
        return can_proceed(self.approved)

    @property
    def in_deleted_state(self):
        return can_proceed(self.deleted)

    def dispatch(self, *args, **kwargs: object):
        return super(LifecycleMixin, self).dispatch(*args, **kwargs)


class PublishableMixin(LifecycleMixin):
    """
    A mixin applied to any class that can be published.
    """

    publication_requested = 'publication_requested'
    published = 'published'
    withdrawn = 'withdrawn'
    deleted = 'deleted'

    LIFECYCLE_STATES = LifecycleMixin.LIFECYCLE_STATES + (
        (publication_requested, _('publication requested')),
        (published, _('published')),
        (withdrawn, _('withdrawn')),
    )

    publication_requested_at = models.DateTimeField(
        _("publication requested at"),
        blank=True,
        null=True
    )
    publication_requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_publication_requestor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    published_at = models.DateTimeField(
        _("published at"),
        blank=True,
        null=True
    )
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    withdrawn_at = models.DateTimeField(
        _("withdrawn at"),
        blank=True,
        null=True
    )
    withdrawn_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_withdrawer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    # FSM transitions

    @transition(field=LifecycleMixin.status,
                source=[LifecycleMixin.draft, LifecycleMixin.submitted, LifecycleMixin.approved, publication_requested,
                        withdrawn], target=deleted)
    def delete(self):
        pass

    @transition(field=LifecycleMixin.status, source=LifecycleMixin.approved, target=publication_requested)
    def publication_requested(self):
        pass

    @transition(field=LifecycleMixin.status, source=publication_requested, target=published)
    def published(self):
        pass

    @transition(field=LifecycleMixin.status, source=published, target=withdrawn)
    def withdrawn(self):
        pass

    # FSM states

    @property
    def in_publication_requested_state(self):
        return can_proceed(self.publication_requested)

    @property
    def in_published_state(self):
        return can_proceed(self.published)

    @property
    def in_withdrawn_state(self):
        return can_proceed(self.withdrawn)

    def dispatch(self, *args, **kwargs: object):
        return super(PublishableMixin, self).dispatch(*args, **kwargs)


class PersistableMixin(PublishableMixin):
    """
        A mixin applied to any class that can be persistently published (e.g. via DOI).
    """

    persistently_published = 'persistently_published'

    LIFECYCLE_STATES = PublishableMixin.LIFECYCLE_STATES + (
        (persistently_published, _('persistently´published')),
    )

    persistently_published_at = models.DateTimeField(
        _("persistently published at"),
        blank=True,
        null=True
    )
    persistently_published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + '_persistently_publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    # FSM transitions

    @transition(field=LifecycleMixin.status, source=PublishableMixin.published,
                target=persistently_published)
    def persistently_published(self):
        pass

    @property
    def in_persistently_published_state(self):
        return can_proceed(self.persistently_published)


class ReviewMixin(models.Model):
    """
        A mixin applied to any class that can be reviewed.
    """

    reviewed_at_time = models.DateTimeField(
        _("reviewed at"),
        auto_now=True,
        null=True,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s' + 'reviewer',
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("modifier_help"),
    )

    class Meta:
        abstract = True


# USER / PERMISSIONS
# ----------------------------------------------------------------------------

class SuperUserRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a super user
    (i.e. `is_superuser` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(
                request,
                'Error: Administrator permission is required to access this resource')
            return redirect(reverse('user_login'))
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)


class IsSuperuserMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class UserRequired(object):
    """
    Only allow a logged in user for flagging
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserRequired, self).dispatch(request, *args, **kwargs)
