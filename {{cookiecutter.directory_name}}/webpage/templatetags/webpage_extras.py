import json
import re

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from typing import Any

from webpage.metadata import PROJECT_METADATA as PM

register = template.Library()


@register.filter()
def class_name(value):
    return value.__class__.__name__


@register.simple_tag
def settings_value(name):
    # pass settings value tp template
    return getattr(settings, name, "")


@register.simple_tag
def projects_metadata(key):
    return PM[key]


@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    inspired by https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
    call in template like e.g. 'get_verbose_name <classname> "<fieldname>" '
    """
    try:
        label = instance._meta.get_field(field_name).verbose_name
    except Exception as e:  # noqa: F841
        label = None
    if label:
        return "{}".format(label)
    else:
        return "No verbose name for '{}' provided".format(field_name)


@register.simple_tag
def get_help_text(instance, field_name):
    """
    Returns help_text for a field.
    inspired by https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
    call in template like e.g.  get_help_text <classname> "<fieldname>"
    """
    try:
        label = instance._meta.get_field(field_name).help_text
    except Exception as e:  # noqa: F841
        label = None
    if label:
        return "{}".format(label)
    else:
        return "No helptext for '{}' provided".format(field_name)


@register.inclusion_tag('webpage/tags/social_media.html', takes_context=True)
def social_media(context):
    """ looks for a 'social_media' key in webpage.py and renders html-tags for each entry """
    values = {}
    values['sm_items'] = PM['social_media']
    values['sm_len'] = len(PM['social_media'])
    return values


@register.simple_tag
def current_domain():
    return 'http://%s' % Site.objects.get_current().domain


@register.filter
def replace_string(string, args):
    search = args.split(args[0])[1]
    replace = args.split(args[0])[2]
    return re.sub(search, replace, string)


@register.filter
def display_label(bf):
    """Returns the display value of a BoundField"""
    return dict(bf.field.choices).get(bf.data, '')


@register.filter
def display_value(value: Any, arg: str = None) -> str:
    """
    human readable choices
    Returns the display value of a BoundField or other form fields
    https://stackoverflow.com/questions/1105638/django-templates-verbose-version-of-a-choice
    """
    if not arg:  # attempt to auto-parse
        # Returning regular field's value
        if not hasattr(value.field, 'choices'): return value.value()
        # Display select value for BoundField / Multiselect field
        # This is used to get_..._display() for a read-only form-field
        # which is not rendered as Input, but instead as text
        return list(value.field.choices)[value.value()][1]
    # usage: "{{"  field|display_value:<arg> "}}"
    if hasattr(value, 'get_' + str(arg) + '_display'):
        return getattr(value, 'get_%s_display' % arg)()
    elif hasattr(value, str(arg)):
        if callable(getattr(value, str(arg))):
            return getattr(value, arg)()
        return getattr(value, arg)
    return value.get(arg) or ''


@register.filter(is_safe=True)
def js(obj):
    """
    properly escape json with complex data structures (e.g. for use in javascript)
    use:  var a = "{{" a | js "}}";
    Please note:
    Bandit issue: [B703:django_mark_safe] Potential XSS on mark_safe function.
    Bandit issue: [B308:blacklist] Use of mark_safe() may expose cross-site scripting vulnerabilities and should be reviewed.
    """
    return mark_safe(json.dumps(obj))


@register.simple_tag
def get_force_script_name():
    if settings.FORCE_SCRIPT_NAME:
        return settings.FORCE_SCRIPT_NAME
    else:
        return ''
