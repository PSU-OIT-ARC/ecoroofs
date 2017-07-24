from django.conf import settings
from django.contrib.gis.admin.options import GeoModelAdmin as BaseGeoModelAdmin
from django.contrib.gis.admin.widgets import OpenLayersWidget


class BingOpenLayersWidget(OpenLayersWidget):

    def get_context(self, name, value, attrs):
        attrs['bing_key'] = settings.MAP.bing.key
        return super().get_context(name, value, attrs)


class GeoModelAdmin(BaseGeoModelAdmin):
    default_lon = settings.MAP.view.center[0]
    default_lat = settings.MAP.view.center[1]
    default_zoom = 12
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    map_template = 'admin/location_openlayers.html'
    map_srid = "900913"
    widget = BingOpenLayersWidget
