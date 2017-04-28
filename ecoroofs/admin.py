from django.conf import settings
from django.contrib.gis.admin.options import GeoModelAdmin as BaseGeoModelAdmin


class GeoModelAdmin(BaseGeoModelAdmin):

    default_lon = settings.MAP.view.center[0]
    default_lat = settings.MAP.view.center[1]
    default_zoom = 11
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
