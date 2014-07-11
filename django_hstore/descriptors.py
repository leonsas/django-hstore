from django.db import models
from .dict import *


__all__ = [
    'HStoreDescriptor',
    'HStoreReferenceDescriptor',
    'HStoreModeledDescriptor'
]


class HStoreDescriptor(models.fields.subclassing.Creator):
    _dict_class = HStoreDict
    
    def __set__(self, obj, value):
        value = self.field.to_python(value)
        if isinstance(value, dict):
            value = self._dict_class(
                value=value, field=self.field, instance=obj
            )
        obj.__dict__[self.field.name] = value


class HStoreReferenceDescriptor(HStoreDescriptor):
    _dict_class = HStoreReferenceDictionary


class HStoreModeledDescriptor(HStoreDescriptor):
    _dict_class = HStoreModeledDictionary
    
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema')
        super(HStoreModeledDescriptor, self).__init__(*args, **kwargs)
    
    def __set__(self, obj, value):
        value = self.field.to_python(value)
        if isinstance(value, dict):
            value = self._dict_class(
                value=value, field=self.field, instance=obj, schema=self.schema
            )
        obj.__dict__[self.field.name] = value