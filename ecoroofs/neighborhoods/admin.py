from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from arcutils import admin

from ..admin import GeoModelAdmin
from .models import *  # noqa


class NeighborhoodAdmin(GeoModelAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            return super().change_view(request, object_id, form_url='', extra_context=None)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        url = reverse('admin:{app_label}_{model_name}_changelist'.format_map(locals()))
        return HttpResponseRedirect(url)

    def get_actions(self, request):
        if request.user.is_superuser:
            return super().get_actions(request)

    def get_list_display_links(self, request, list_display):
        if request.user.is_superuser:
            return super().get_list_display_links(request, list_display)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.cas_site.register(Neighborhood, NeighborhoodAdmin)
