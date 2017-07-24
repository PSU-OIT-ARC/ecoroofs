from django.db import models
from django.core.urlresolvers import reverse

from arcutils.decorators import cached_property, CachedPropertyInvalidatorMixin

from ..models import BaseModel


class Page(BaseModel, CachedPropertyInvalidatorMixin):

    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    published = models.BooleanField(default=False)

    @cached_property('slug')
    def path(self):
        return reverse('page-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '{self.name} at {self.path}'.format(self=self)
