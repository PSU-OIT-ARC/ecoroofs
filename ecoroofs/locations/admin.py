from arcutils import admin

from ..admin import GeoModelAdmin
from .models import *  # noqa


admin.cas_site.register(Location, GeoModelAdmin)
admin.cas_site.register(BuildingUse)
admin.cas_site.register(Contractor)
admin.cas_site.register(Watershed)
admin.cas_site.register(Contractor)
