#from __future__ import unicode_literals
#
#import copy
#import datetime
#import decimal
#import math
#import warnings
#from base64 import b64decode, b64encode
#from itertools import tee
#
#from django.db import connection
#from django.db.models.loading import get_model
#from django.db.models.query_utils import QueryWrapper
#from django.conf import settings
#from django import forms
#from django.core import exceptions, validators
#from django.utils.datastructures import DictWrapper
#from django.utils.dateparse import parse_date, parse_datetime, parse_time
#from django.utils.functional import curry, total_ordering
#from django.utils.itercompat import is_iterator
#from django.utils.text import capfirst
#from django.utils import timezone
#from django.utils.translation import ugettext_lazy as _
#from django.utils.encoding import smart_text, force_text, force_bytes
#from django.utils.ipv6 import clean_ipv6_address
#from django.utils import six
#
#class Empty(object):
#    pass
#
#class NOT_PROVIDED:
#    pass
#
## The values to use for "blank" in SelectFields. Will be appended to the start
## of most "choices" lists.
#BLANK_CHOICE_DASH = [("", "---------")]
#
#def _load_field(app_label, model_name, field_name):
#    return get_model(app_label, model_name)._meta.get_field_by_name(field_name)[0]
#
#class FieldDoesNotExist(Exception):
#    pass

# A guide to Field parameters:
#
#   * name:      The name of the field specifed in the model.
#   * attname:   The attribute to use on the model object. This is the same as
#                "name", except in the case of ForeignKeys, where "_id" is
#                appended.
#   * db_column: The db_column specified in the model (or None).
#   * column:    The database column for this field. This is the same as
#                "attname", except if db_column is specified.
#
# Code that introspects values, or does other dynamic things, should use
# attname. For example, this gets the primary key value of object "obj":
#
#     getattr(obj, opts.pk.attname)

#def _empty(of_cls):
#    new = Empty()
#    new.__class__ = of_cls
#    return new

from django.db.models.fields import Field
from django.core.exceptions import ValidationError


class VirtualField(Field):
    """ Virtual Field """

    # Designates whether empty strings fundamentally are allowed at the
    # database level.
    #empty_strings_allowed = True
    #empty_values = list(validators.EMPTY_VALUES)
    #
    ## These track each time a Field instance is created. Used to retain order.
    ## The auto_creation_counter is used for fields that Django implicitly
    ## creates, creation_counter is used for all user-specified fields.
    #creation_counter = 0
    #auto_creation_counter = -1
    #default_validators = [] # Default set of validators
    #default_error_messages = {
    #    'invalid_choice': _('Value %(value)r is not a valid choice.'),
    #    'null': _('This field cannot be null.'),
    #    'blank': _('This field cannot be blank.'),
    #    'unique': _('%(model_name)s with this %(field_label)s '
    #                'already exists.'),
    #}
    #
    ## Generic field type description, usually overriden by subclasses
    #def _description(self):
    #    return _('Field of type: %(field_type)s') % {
    #        'field_type': self.__class__.__name__
    #    }
    #description = property(_description)
    #
    def __init__(self, *args, **kwargs):
        try:
            self.hstore_field_name = kwargs.pop('hstore_field_name')
        except KeyError:
            raise ValueError('missing hstore_field_name keyword argument')
        super(VirtualField, self).__init__(*args, **kwargs)
    #def __init__(self, verbose_name=None, name=None, primary_key=False,
    #        max_length=None, unique=False, blank=False, null=False,
    #        db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
    #        serialize=True, unique_for_date=None, unique_for_month=None,
    #        unique_for_year=None, choices=None, help_text='', db_column=None,
    #        db_tablespace=None, auto_created=False, validators=[],
    #        error_messages=None):
    #    self.name = name
    #    self.verbose_name = verbose_name
    #    self.primary_key = primary_key
    #    self.max_length, self._unique = max_length, unique
    #    self.blank, self.null = blank, null
    #    self.rel = rel
    #    self.default = default
    #    self.editable = editable
    #    self.serialize = serialize
    #    self.unique_for_date, self.unique_for_month = (unique_for_date,
    #                                                   unique_for_month)
    #    self.unique_for_year = unique_for_year
    #    self._choices = choices or []
    #    self.help_text = help_text
    #    self.db_column = db_column
    #    self.db_tablespace = db_tablespace or settings.DEFAULT_INDEX_TABLESPACE
    #    self.auto_created = auto_created
    #
    #    # Set db_index to True if the field has a relationship and doesn't
    #    # explicitly set db_index.
    #    self.db_index = db_index
    #
    #    # Adjust the appropriate creation counter, and save our local copy.
    #    if auto_created:
    #        self.creation_counter = VirtualField.auto_creation_counter
    #        VirtualField.auto_creation_counter -= 1
    #    else:
    #        self.creation_counter = VirtualField.creation_counter
    #        VirtualField.creation_counter += 1
    #
    #    self.validators = self.default_validators + validators
    #
    #    messages = {}
    #    for c in reversed(self.__class__.__mro__):
    #        messages.update(getattr(c, 'default_error_messages', {}))
    #    messages.update(error_messages or {})
    #    self.error_messages = messages
    #
    #def __eq__(self, other):
    #    # Needed for @total_ordering
    #    if isinstance(other, VirtualField):
    #        return self.creation_counter == other.creation_counter
    #    return NotImplemented
    #
    #def __lt__(self, other):
    #    # This is needed because bisect does not take a comparison function.
    #    if isinstance(other, VirtualField):
    #        return self.creation_counter < other.creation_counter
    #    return NotImplemented
    #
    #def __hash__(self):
    #    return hash(self.creation_counter)
    #
    #def __deepcopy__(self, memodict):
    #    # We don't have to deepcopy very much here, since most things are not
    #    # intended to be altered after initial creation.
    #    obj = copy.copy(self)
    #    if self.rel:
    #        obj.rel = copy.copy(self.rel)
    #        if hasattr(self.rel, 'field') and self.rel.field is self:
    #            obj.rel.field = obj
    #    memodict[id(self)] = obj
    #    return obj
    #
    #def __copy__(self):
    #    # We need to avoid hitting __reduce__, so define this
    #    # slightly weird copy construct.
    #    obj = Empty()
    #    obj.__class__ = self.__class__
    #    obj.__dict__ = self.__dict__.copy()
    #    return obj
    #
    #def __reduce__(self):
    #    """
    #    Pickling should return the model._meta.fields instance of the field,
    #    not a new copy of that field. So, we use the app cache to load the
    #    model and then the field back.
    #    """
    #    if not hasattr(self, 'model'):
    #        # Fields are sometimes used without attaching them to models (for
    #        # example in aggregation). In this case give back a plain field
    #        # instance. The code below will create a new empty instance of
    #        # class self.__class__, then update its dict with self.__dict__
    #        # values - so, this is very close to normal pickle.
    #        return _empty, (self.__class__,), self.__dict__
    #    if self.model._deferred:
    #        # Deferred model will not be found from the app cache. This could
    #        # be fixed by reconstructing the deferred model on unpickle.
    #        raise RuntimeError("Fields of deferred models can't be reduced")
    #    return _load_field, (self.model._meta.app_label, self.model._meta.object_name,
    #                         self.name)
    #
    #def to_python(self, value):
    #    """
    #    Converts the input value into the expected Python data type, raising
    #    django.core.exceptions.ValidationError if the data can't be converted.
    #    Returns the converted value. Subclasses should override this.
    #    """
    #    return value
    #
    #def run_validators(self, value):
    #    if value in self.empty_values:
    #        return
    #
    #    errors = []
    #    for v in self.validators:
    #        try:
    #            v(value)
    #        except exceptions.ValidationError as e:
    #            if hasattr(e, 'code') and e.code in self.error_messages:
    #                e.message = self.error_messages[e.code]
    #            errors.extend(e.error_list)
    #
    #    if errors:
    #        raise exceptions.ValidationError(errors)
    #
    #def validate(self, value, model_instance):
    #    """
    #    Validates value and throws ValidationError. Subclasses should override
    #    this to provide validation logic.
    #    """
    #    if not self.editable:
    #        # Skip validation for non-editable fields.
    #        return
    #
    #    if self._choices and value not in self.empty_values:
    #        for option_key, option_value in self.choices:
    #            if isinstance(option_value, (list, tuple)):
    #                # This is an optgroup, so look inside the group for
    #                # options.
    #                for optgroup_key, optgroup_value in option_value:
    #                    if value == optgroup_key:
    #                        return
    #            elif value == option_key:
    #                return
    #        raise exceptions.ValidationError(
    #            self.error_messages['invalid_choice'],
    #            code='invalid_choice',
    #            params={'value': value},
    #        )
    #
    #    if value is None and not self.null:
    #        raise exceptions.ValidationError(self.error_messages['null'], code='null')
    #
    #    if not self.blank and value in self.empty_values:
    #        raise exceptions.ValidationError(self.error_messages['blank'], code='blank')
    #
    #def clean(self, value, model_instance):
    #    """
    #    Convert the value's type and run validation. Validation errors
    #    from to_python and validate are propagated. The correct value is
    #    returned if no error is raised.
    #    """
    #    value = self.to_python(value)
    #    self.validate(value, model_instance)
    #    self.run_validators(value)
    #    return value

    #def db_type(self, connection):
    #    """
    #    Returns the database column data type for this field, for the provided
    #    connection.
    #    """
    #    return None

    #def set_attributes_from_name(self, name):
    #    if not self.name:
    #        self.name = name
    #    self.attname, self.column = self.get_attname_column()
    #    if self.verbose_name is None and self.name:
    #        self.verbose_name = self.name.replace('_', ' ')
    
    #@property
    #def unique(self):
    #    return False
    
    def contribute_to_class(self, cls, name, virtual_only=True):
        super(VirtualField, self).contribute_to_class(cls, name, virtual_only)
        
        # Connect myself as the descriptor for this field
        setattr(cls, name, self)
    
    # begin descriptor methods
    
    def __get__(self, instance, instance_type=None):
        """
        retrieve value from hstore dictionary
        """
        return getattr(instance, self.hstore_field_name).get(self.name)
    
    def __set__(self, instance, value):
        """
        set value on hstore dictionary
        """
        hstore_dictionary = getattr(instance, self.hstore_field_name)
        hstore_dictionary[self.name] = value
    
    # end descriptor methods
    
    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.
        """
        hstore_field = getattr(obj, self.hstore_field_name)
        return hstore_field[self.attname]
    
    def save_form_data(self, instance, data):
        hstore_field = getattr(instance, self.hstore_field_name)
        hstore_field[self.attname] = data
        setattr(instance, self.hstore_field_name, hstore_field)
        # DELETEME
        print instance.data
    
    #def get_attname(self):
    #    return self.name

    #def get_attname_column(self):
    #    return self.get_attname(), None

    #def get_cache_name(self):
    #    return '_%s_cache' % self.name
    #
    #def get_internal_type(self):
    #    return self.__class__.__name__
    #
    def __setitem__(self, name, subfield):
        print 'hey'
    #
    #def get_prep_value(self, value):
    #    """
    #    Perform preliminary non-db specific value checks and conversions.
    #    """
    #    return value
    #
    #def get_db_prep_value(self, value, connection, prepared=False):
    #    """Returns field's value prepared for interacting with the database
    #    backend.
    #
    #    Used by the default implementations of ``get_db_prep_save``and
    #    `get_db_prep_lookup```
    #    """
    #    if not prepared:
    #        value = self.get_prep_value(value)
    #    return value
    #
    #def get_db_prep_save(self, value, connection):
    #    """
    #    Returns field's value prepared for saving into a database.
    #    """
    #    return self.get_db_prep_value(value, connection=connection,
    #                                  prepared=False)
    #
    #def get_prep_lookup(self, lookup_type, value):
    #    """
    #    Perform preliminary non-db specific lookup checks and conversions
    #    """
    #    if hasattr(value, 'prepare'):
    #        return value.prepare()
    #    if hasattr(value, '_prepare'):
    #        return value._prepare()
    #
    #    if lookup_type in (
    #            'iexact', 'contains', 'icontains',
    #            'startswith', 'istartswith', 'endswith', 'iendswith',
    #            'month', 'day', 'week_day', 'hour', 'minute', 'second',
    #            'isnull', 'search', 'regex', 'iregex',
    #        ):
    #        return value
    #    elif lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
    #        return self.get_prep_value(value)
    #    elif lookup_type in ('range', 'in'):
    #        return [self.get_prep_value(v) for v in value]
    #    elif lookup_type == 'year':
    #        try:
    #            return int(value)
    #        except ValueError:
    #            raise ValueError("The __year lookup type requires an integer "
    #                             "argument")
    #
    #    raise TypeError("Field has invalid lookup: %s" % lookup_type)

    #def get_db_prep_lookup(self, lookup_type, value, connection,
    #                       prepared=False):
    #    """
    #    Returns field's value prepared for database lookup.
    #    """
    #    return []
    #    if not prepared:
    #        value = self.get_prep_lookup(lookup_type, value)
    #        prepared = True
    #    if hasattr(value, 'get_compiler'):
    #        value = value.get_compiler(connection=connection)
    #    if hasattr(value, 'as_sql') or hasattr(value, '_as_sql'):
    #        # If the value has a relabeled_clone method it means the
    #        # value will be handled later on.
    #        if hasattr(value, 'relabeled_clone'):
    #            return value
    #        if hasattr(value, 'as_sql'):
    #            sql, params = value.as_sql()
    #        else:
    #            sql, params = value._as_sql(connection=connection)
    #        return QueryWrapper(('(%s)' % sql), params)
    #    
    #    if lookup_type in ('month', 'day', 'week_day', 'hour', 'minute',
    #                       'second', 'search', 'regex', 'iregex'):
    #        return [value]
    #    elif lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
    #        return [self.get_db_prep_value(value, connection=connection,
    #                                       prepared=prepared)]
    #    elif lookup_type in ('range', 'in'):
    #        return [self.get_db_prep_value(v, connection=connection,
    #                                       prepared=prepared) for v in value]
    #    elif lookup_type in ('contains', 'icontains'):
    #        return ["%%%s%%" % connection.ops.prep_for_like_query(value)]
    #    elif lookup_type == 'iexact':
    #        return [connection.ops.prep_for_iexact_query(value)]
    #    elif lookup_type in ('startswith', 'istartswith'):
    #        return ["%s%%" % connection.ops.prep_for_like_query(value)]
    #    elif lookup_type in ('endswith', 'iendswith'):
    #        return ["%%%s" % connection.ops.prep_for_like_query(value)]
    #    elif lookup_type == 'isnull':
    #        return []
    #    elif lookup_type == 'year':
    #        if isinstance(self, DateTimeField):
    #            return connection.ops.year_lookup_bounds_for_datetime_field(value)
    #        elif isinstance(self, DateField):
    #            return connection.ops.year_lookup_bounds_for_date_field(value)
    #        else:
    #            return [value]          # this isn't supposed to happen

    #def has_default(self):
    #    """
    #    Returns a boolean of whether this field has a default value.
    #    """
    #    return self.default is not NOT_PROVIDED
    #
    #def get_default(self):
    #    """
    #    Returns the default value for this field.
    #    """
    #    if self.has_default():
    #        if callable(self.default):
    #            return self.default()
    #        return force_text(self.default, strings_only=True)
    #    if (not self.empty_strings_allowed or (self.null and
    #               not connection.features.interprets_empty_strings_as_nulls)):
    #        return None
    #    return ""
    #
    #def get_validator_unique_lookup_type(self):
    #    return '%s__exact' % self.name
    #
    #def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
    #    """Returns choices with a default blank choices included, for use
    #    as SelectField choices for this field."""
    #    first_choice = blank_choice if include_blank else []
    #    if self.choices:
    #        return first_choice + list(self.choices)
    #    rel_model = self.rel.to
    #    if hasattr(self.rel, 'get_related_field'):
    #        lst = [(getattr(x, self.rel.get_related_field().attname),
    #                    smart_text(x))
    #               for x in rel_model._default_manager.complex_filter(
    #                   self.rel.limit_choices_to)]
    #    else:
    #        lst = [(x._get_pk_val(), smart_text(x))
    #               for x in rel_model._default_manager.complex_filter(
    #                   self.rel.limit_choices_to)]
    #    return first_choice + lst
    #
    #def get_choices_default(self):
    #    return self.get_choices()
    #
    #def get_flatchoices(self, include_blank=True,
    #                    blank_choice=BLANK_CHOICE_DASH):
    #    """
    #    Returns flattened choices with a default blank choice included.
    #    """
    #    first_choice = blank_choice if include_blank else []
    #    return first_choice + list(self.flatchoices)
    #
    #def _get_val_from_obj(self, obj):
    #    if obj is not None:
    #        return getattr(obj, self.attname)
    #    else:
    #        return self.get_default()
    #
    #def value_to_string(self, obj):
    #    """
    #    Returns a string value of this field from the passed obj.
    #    This is used by the serialization framework.
    #    """
    #    return smart_text(self._get_val_from_obj(obj))
    #
    #def bind(self, fieldmapping, original, bound_field_class):
    #    return bound_field_class(self, fieldmapping, original)
    #
    #def _get_choices(self):
    #    if is_iterator(self._choices):
    #        choices, self._choices = tee(self._choices)
    #        return choices
    #    else:
    #        return self._choices
    #choices = property(_get_choices)
    #
    #def _get_flatchoices(self):
    #    """Flattened version of choices tuple."""
    #    flat = []
    #    for choice, value in self.choices:
    #        if isinstance(value, (list, tuple)):
    #            flat.extend(value)
    #        else:
    #            flat.append((choice,value))
    #    return flat
    #flatchoices = property(_get_flatchoices)
    #
    #def save_form_data(self, instance, data):
    #    setattr(instance, self.name, data)
    #
    #def formfield(self, form_class=None, choices_form_class=None, **kwargs):
    #    """
    #    Returns a django.forms.Field instance for this database Field.
    #    """
    #    defaults = {'required': not self.blank,
    #                'label': capfirst(self.verbose_name),
    #                'help_text': self.help_text}
    #    if self.has_default():
    #        if callable(self.default):
    #            defaults['initial'] = self.default
    #            defaults['show_hidden_initial'] = True
    #        else:
    #            defaults['initial'] = self.get_default()
    #    if self.choices:
    #        # Fields with choices get special treatment.
    #        include_blank = (self.blank or
    #                         not (self.has_default() or 'initial' in kwargs))
    #        defaults['choices'] = self.get_choices(include_blank=include_blank)
    #        defaults['coerce'] = self.to_python
    #        if self.null:
    #            defaults['empty_value'] = None
    #        if choices_form_class is not None:
    #            form_class = choices_form_class
    #        else:
    #            form_class = forms.TypedChoiceField
    #        # Many of the subclass-specific formfield arguments (min_value,
    #        # max_value) don't apply for choice fields, so be sure to only pass
    #        # the values that TypedChoiceField will understand.
    #        for k in list(kwargs):
    #            if k not in ('coerce', 'empty_value', 'choices', 'required',
    #                         'widget', 'label', 'initial', 'help_text',
    #                         'error_messages', 'show_hidden_initial'):
    #                del kwargs[k]
    #    defaults.update(kwargs)
    #    if form_class is None:
    #        form_class = forms.CharField
    #    return form_class(**defaults)
    #
    
    #
    #def __repr__(self):
    #    """
    #    Displays the module, class and name of the field.
    #    """
    #    path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
    #    name = getattr(self, 'name', None)
    #    if name is not None:
    #        return '<%s: %s>' % (path, name)
    #    return '<%s>' % path