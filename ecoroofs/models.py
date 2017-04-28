import uuid

from django.db import models
from django.utils.text import slugify


class UUIDPrimaryKeyField(models.UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['editable'] = False
        kwargs['primary_key'] = True
        kwargs.setdefault('default', uuid.uuid4)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('blank', None)
        kwargs.pop('editable', None)
        kwargs.pop('primary_key', None)
        return name, path, args, kwargs


class UniqueDerivedSlugField(models.SlugField):

    default_source_field = 'name'

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('max_length', 255)
        self.source_field = kwargs.pop('source_field', self.default_source_field)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.source_field != self.default_source_field:
            kwargs['source_field'] = self.source_field
        kwargs.pop('unique', None)
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        source_value = getattr(model_instance, self.source_field)
        slug_value = slugify(source_value)
        return slug_value


class BaseModel(models.Model):

    class Meta:
        abstract = True
        ordering = ['name']

    id = UUIDPrimaryKeyField()
    name = models.CharField(max_length=255, unique=True)
    slug = UniqueDerivedSlugField(source_field='name')

    def __str__(self):
        return self.name
