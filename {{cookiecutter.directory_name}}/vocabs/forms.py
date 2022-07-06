import re

from django import forms
from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML, ButtonHolder
from crispy_forms.bootstrap import *
from dal import autocomplete
from mptt.forms import TreeNodeChoiceField

from core.forms import *
from core.custom_layout_object import *

from .models import *
from .endpoints import *


class UploadFileForm(forms.Form):
    file = forms.FileField()
    language = forms.CharField(
        max_length=3, required=True,
        help_text="Specify the main language of your vocabulary (in format ISO 639-1 or ISO 639-3)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. en'})
    )

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'upload', css_id='uploadFile'), )


######################################################################
#   Classes  to store titles and descriptions for ConceptScheme
######################################################################


# We also want to verify that all formsets have both fields a name and a language filled out.
# We could simply set the fields as required on the form itself,
# however this will prevent our users from submitting empty forms,
# which is not the behaviour we’re looking for here. From a usability perspective, it would be better
# to simply ignore forms that are completely empty, raising errors only if a form is partially incomplete.

class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(CustomInlineFormSet, self).clean()
        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                language = form.cleaned_data['language']
                # Check that formset has both fields - a name and a language - filled out
                if name and not language:
                    raise forms.ValidationError(
                        'All names must have a lanaguge.'
                    )
                elif language and not name:
                    raise forms.ValidationError(
                        'All languages must have a name.'
                    )


class ConceptSchemeTitleForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptSchemeTitle._meta.get_field('name').verbose_name,
        help_text=ConceptSchemeTitle._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptSchemeTitle._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptSchemeTitle._meta.get_field('language').verbose_name,
        help_text=ConceptSchemeTitle._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptSchemeTitle._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptSchemeTitleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptSchemeTitle
        exclude = ()


ConceptSchemeTitleFormSet = inlineformset_factory(
    SkosConceptScheme, ConceptSchemeTitle,
    form=ConceptSchemeTitleForm,
    fields=['name', 'language'], extra=1, can_delete=True
)


class ConceptSchemeDescriptionForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptSchemeDescription._meta.get_field('name').verbose_name,
        help_text=ConceptSchemeDescription._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptSchemeDescription._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptSchemeDescription._meta.get_field('language').verbose_name,
        help_text=ConceptSchemeDescription._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptSchemeDescription._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptSchemeDescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptSchemeDescription
        exclude = ()


ConceptSchemeDescriptionFormSet = inlineformset_factory(
    SkosConceptScheme, ConceptSchemeDescription,
    form=ConceptSchemeDescriptionForm,
    fields=['name', 'language'], extra=1, can_delete=True
)


class ConceptSchemeSourceForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptSchemeSource._meta.get_field('name').verbose_name,
        help_text=ConceptSchemeSource._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptSchemeSource._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptSchemeSource._meta.get_field('language').verbose_name,
        help_text=ConceptSchemeSource._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptSchemeSource._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptSchemeSourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptSchemeSource
        exclude = ()


ConceptSchemeSourceFormSet = inlineformset_factory(
    SkosConceptScheme, ConceptSchemeSource, form=ConceptSchemeSourceForm,
    fields=['name', 'language'],
    extra=1, can_delete=True
)


######################################################################
#
# SkosConceptScheme
#
######################################################################


class SkosConceptSchemeForm(forms.ModelForm):
    class Meta:
        model = SkosConceptScheme
        exclude = ['created_by', ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'title_lang': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'identifier': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'license': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'owner': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'publisher': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'creator': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'contributor': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'relation': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'subject': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'coverage': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'language': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'curator': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:user-autocomplete'
            ),
            'version': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'legacy_id': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'date_issued': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SkosConceptSchemeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('title_lang'),
                Field('curator'),
                Field('owner'),
                Field('license'),
                Accordion(
                    AccordionGroup(
                        'Recommended Information',
                        Accordion(
                            AccordionGroup(
                                'Titles in other languages',
                                Fieldset('',
                                         Formset('titles'), css_class="formset-div"),
                                # TODO: active=False causes remove button to be hidden
                                # active=False,
                                # <div id="{{ div.css_id }}" class="{% if div.css_class %}{{ div.css_class }}{% endif %}" role="tabpanel"
                                #          aria-labelledby="{{ div.css_id }}" data-parent="#{{ div.data_parent }}">
                                # css_class="collapse collapsed"
                            ),
                            Accordion(
                                AccordionGroup(
                                    'Descriptions',
                                    Fieldset('',
                                             Formset('descriptions'), css_class="formset-div"),
                                )
                            ),
                            Accordion(
                                AccordionGroup(
                                    'Agents',
                                    Field('creator'),
                                    Field('contributor'),
                                    Field('publisher'),
                                    # active=False,
                                )
                            ),
                            Accordion(
                                AccordionGroup(
                                    'Versioning',
                                    Field('version'),
                                    Field('legacy_id'),
                                    Field('date_issued', placeholder="YYYY-MM-DD"),
                                )
                            ),
                            Accordion(
                                AccordionGroup(
                                    'Other descriptive information',
                                    Field('subject'),
                                    Field('coverage'),
                                    Field('language'),
                                    Field('identifier', placeholder="https://example.org/vocabulary-unique-title"),
                                    Field('relation'),
                                )
                            ),
                        ),
                        css_class="recommended"
                    ),
                ),
                Accordion(
                    AccordionGroup(
                        'Optional Information',
                        Accordion(
                            AccordionGroup(
                                'Source Information',
                                Fieldset('',
                                         Formset('sources'), css_class="formset-div"),
                                # active=False,
                            ),
                        ),
                    ),
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )


class SkosConceptSchemeFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkosConceptSchemeFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                '',
                Field('title', css_class='form-control'),
                Field('creator', css_class='form-control'),
                css_id="basic_search_fields"
            ),
        )


######################################################################
#   Classes  to store labels and notes for Collection
######################################################################

class CollectionLabelForm(forms.ModelForm):
    name = forms.CharField(
        label=CollectionLabel._meta.get_field('name').verbose_name,
        help_text=CollectionLabel._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=CollectionLabel._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=CollectionLabel._meta.get_field('language').verbose_name,
        help_text=CollectionLabel._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=CollectionLabel._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CollectionLabelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = CollectionLabel
        exclude = ()


CollectionLabelFormSet = inlineformset_factory(
    SkosCollection, CollectionLabel, form=CollectionLabelForm,
    fields=['name', 'label_type', 'language'],
    extra=1, can_delete=True
)


class CollectionNoteForm(forms.ModelForm):
    name = forms.CharField(
        label=CollectionNote._meta.get_field('name').verbose_name,
        help_text=CollectionNote._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=CollectionNote._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=CollectionNote._meta.get_field('language').verbose_name,
        help_text=CollectionNote._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=CollectionNote._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CollectionNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = CollectionNote
        exclude = ()


CollectionNoteFormSet = inlineformset_factory(
    SkosCollection, CollectionNote, form=CollectionNoteForm,
    fields=['name', 'note_type', 'language'],
    extra=1, can_delete=True
)


class CollectionSourceForm(forms.ModelForm):
    name = forms.CharField(
        label=CollectionSource._meta.get_field('name').verbose_name,
        help_text=CollectionSource._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=CollectionSource._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=CollectionSource._meta.get_field('language').verbose_name,
        help_text=CollectionSource._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=CollectionSource._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CollectionSourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = CollectionSource
        exclude = ()


CollectionSourceFormSet = inlineformset_factory(
    SkosCollection, CollectionSource, form=CollectionSourceForm,
    fields=['name', 'language'],
    extra=1, can_delete=True
)


######################################################################
#
# SkosCollection
#
######################################################################

class SkosCollectionForm(forms.ModelForm):
    class Meta:
        model = SkosCollection
        exclude = ['created_by', ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'name_lang': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'legacy_id': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'scheme': autocomplete.ModelSelect2(
                url='vocabs-ac:skosconceptscheme-autocomplete'
            ),
            'creator': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'contributor': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SkosCollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('label_lang'),
                HTML('<h4 class="form-headline">Other Labels</h4>'),
                Fieldset('',
                         Formset('labels'), css_class="formset-div"),
                Field('scheme'),
                Accordion(
                    AccordionGroup(
                        'Recommended Information',
                        HTML('<h4 class="form-headline">Agents</h4>'),
                        Field('creator'),
                        Field('contributor'),
                        HTML('<h4 class="form-headline">Identifier</h4>'),
                        Field('legacy_id'),
                        HTML('<h4 class="form-headline">Notes</h4>'),
                        Fieldset('',
                                 Formset('notes'), css_class="formset-div"),
                    ),
                ),
                Accordion(
                    AccordionGroup(
                        'Optional Information',
                        HTML('<h4 class="form-headline">Source Information/h4>'),
                        Fieldset('',
                                 Formset('sources'), css_class="formset-div"),
                    ),
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )


class SkosCollectionFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(SkosCollectionFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                '',
                Field('name', css_class='form-control'),
                Field('creator', css_class='form-control'),
                Field('scheme', css_class='form-control'),
                Field('has_members__pref_label', css_class='form-control'),
                css_id="basic_search_fields"
            ),
        )


######################################################################
#   Classes  to store labels, notes and sources for Concept
######################################################################

class ConceptLabelForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptLabel._meta.get_field('name').verbose_name,
        help_text=ConceptLabel._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptLabel._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptLabel._meta.get_field('language').verbose_name,
        help_text=ConceptLabel._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptLabel._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptLabelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptLabel
        exclude = ()


ConceptLabelFormSet = inlineformset_factory(
    SkosConcept, ConceptLabel, form=ConceptLabelForm,
    fields=['name', 'label_type', 'language'],
    extra=1, can_delete=True
)


class ConceptNoteForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptNote._meta.get_field('name').verbose_name,
        help_text=ConceptNote._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptNote._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptNote._meta.get_field('language').verbose_name,
        help_text=ConceptNote._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptNote._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptNote
        exclude = ()


ConceptNoteFormSet = inlineformset_factory(
    SkosConcept, ConceptNote, form=ConceptNoteForm,
    fields=['name', 'note_type', 'language'],
    extra=1, can_delete=True
)


class ConceptSourceForm(forms.ModelForm):
    name = forms.CharField(
        label=ConceptSource._meta.get_field('name').verbose_name,
        help_text=ConceptSource._meta.get_field('name').help_text,
        error_messages=custom_name_errors(
            field_name=ConceptSource._meta.get_field('name').verbose_name
        ),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    language = forms.CharField(
        label=ConceptSource._meta.get_field('language').verbose_name,
        help_text=ConceptSource._meta.get_field('language').help_text,
        error_messages=custom_lang_errors(
            field_name=ConceptSource._meta.get_field('name').verbose_name
        ),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ConceptSourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'

    class Meta:
        model = ConceptSource
        exclude = ()


ConceptSourceFormSet = inlineformset_factory(
    SkosConcept, ConceptSource, form=ConceptSourceForm,
    fields=['name', 'language'],
    extra=1, can_delete=True
)


######################################################################
#
# SkosConcept
#
######################################################################

class AutocompleteCharField(forms.CharField):
    widget = autocomplete.TagSelect2(
        url='vocabs-ac:external-link-ac',
        forward=['endpoint'],
        attrs={
            'data-placeholder': 'Type at least 3 characters to get autocomplete suggestions ...',
            'data-minimum-input-length': 3,
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = False

    def to_python(self, value):
        """Normalize data to keep only URIs."""
        clean_value = ",".join(re.findall("(?P<url>https?://[^\s\,]+)", value))
        return clean_value


class SkosConceptForm(forms.ModelForm):
    broader_concept = TreeNodeChoiceField(
        queryset=SkosConcept.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='vocabs-ac:skosconcept-autocomplete',
            forward=['scheme']
        ),
        help_text=SkosConcept._meta.get_field('broader_concept').help_text,
        required=False,
        label=SkosConcept._meta.get_field('broader_concept').verbose_name,
    )
    collection = forms.ModelMultipleChoiceField(
        queryset=SkosCollection.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='vocabs-ac:skoscollection-autocomplete',
            forward=['scheme']
        ),
        help_text=SkosConcept._meta.get_field('collection').help_text,
        required=False,
        label=SkosConcept._meta.get_field('collection').verbose_name,
    )
    endpoint = forms.ChoiceField(
        choices=ENDPOINT_CHOICES, required=False,
        help_text="Select a service to create links to external resources<br>\
        You can also type a matching concept URI in the fields below if it is not provided by current endpoints<br>\
        In that case please note that an external concept's URI should follow the format 'http{s}://example.org/...'"
    )
    related = AutocompleteCharField(
        label=SkosConcept._meta.get_field('related').verbose_name,
        help_text=SkosConcept._meta.get_field('related').help_text
    )
    broad_match = AutocompleteCharField(
        label=SkosConcept._meta.get_field('broad_match').verbose_name,
        help_text=SkosConcept._meta.get_field('broad_match').help_text
    )
    narrow_match = AutocompleteCharField(
        label=SkosConcept._meta.get_field('narrow_match').verbose_name,
        help_text=SkosConcept._meta.get_field('narrow_match').help_text
    )
    exact_match = AutocompleteCharField(
        label=SkosConcept._meta.get_field('exact_match').verbose_name,
        help_text=SkosConcept._meta.get_field('exact_match').help_text
    )
    related_match = AutocompleteCharField(
        label=SkosConcept._meta.get_field('related_match').verbose_name,
        help_text=SkosConcept._meta.get_field('related_match').help_text
    )
    close_match = AutocompleteCharField(
        label=SkosConcept._meta.get_field('close_match').verbose_name,
        help_text=SkosConcept._meta.get_field('close_match').help_text
    )
    needs_review = forms.BooleanField(
        widget=forms.CheckboxInput, required=False,
        help_text=SkosConcept._meta.get_field('needs_review').help_text
    )

    class Meta:
        model = SkosConcept
        exclude = ['created_by', ]
        widgets = {
            'pref_label': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'pref_label_lang': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'language': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'legacy_id': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'creator': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'contributor': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'notation': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'scheme': autocomplete.ModelSelect2(
                url='vocabs-ac:skosconceptscheme-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(SkosConceptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Field('pref_label'),
                Field('pref_label_lang'),
                HTML('<h4 class="form-headline">Schema / Location (Parent)</h4>'),
                Field('scheme'),
                Field('broader_concept'),
                HTML('<h4 class="form-headline">Quality check</h4>'),
                Fieldset('',
                         Field('needs_review'),
                         ),
                Accordion(
                    AccordionGroup(
                        'Recommended Information',
                        HTML('<h4 class="form-headline">Other Labels (preferred, alternate, hidden)</h4>'),
                        HTML(
                            '<p>Please note: every concept may only have one preferred label in one language but can have multiple alternate or hidden labels in any language.</p>'),
                        Fieldset('',
                                 Formset('labels'), css_class="formset-div"),
                        HTML('<h4 class="form-headline">Notes</h4>'),
                        Fieldset('',
                                 Formset('notes'), css_class="formset-div"),
                        HTML('<h4 class="form-headline">Agents</h4>'),
                        Field('creator'),
                        Field('contributor'),
                        HTML('<h4 class="form-headline">Identification</h4>'),
                        Field('notation'),
                        Field('legacy_id'),
                        HTML('<h4 class="form-headline">Semantic Relationships</h4>'),
                        Fieldset('',
                                 Field('endpoint'),
                                 Field('related'),
                                 Field('broad_match'),
                                 Field('narrow_match'),
                                 Field('exact_match'),
                                 Field('related_match'),
                                 Field('close_match'),
                                 ),
                        css_class="recommended"
                    ),
                ),
                Accordion(
                    AccordionGroup(
                        'Optional Information',
                        HTML('<h4 class="form-headline">Source Information</h4>'),
                        Fieldset('',
                                 Formset('sources'), css_class="formset-div"),
                        HTML('<h4 class="form-headline">Collection</h4>'),
                        Field('collection'),
                    )
                ),
                # Field('top_concept'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )
        self.helper.render_required_fields = True


class SkosConceptFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkosConceptFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                '',
                Field('pref_label', css_class='form-control'),
                Field('scheme', css_class='form-control'),
                Field('collection', css_class='form-control'),
                Field('broader_concept', css_class='form-control'),
                css_id="basic_search_fields"
            ),
        )
