from arcutils import admin as arc_admin

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse_lazy

from .models import Page


class AutoSlugField(forms.TextInput):
    class Media:
        js = ('autoSlug/autoSlug.js',)
        css = {
            'all': ('autoSlug/autoSlug.css',)
        }


class PageAdminForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'slug': AutoSlugField(
                attrs={
                    "data-source": "name",
                    "data-endpoint": reverse_lazy('slugify_name')
                }),
        }

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm

arc_admin.cas_site.register(Page, PageAdmin)
