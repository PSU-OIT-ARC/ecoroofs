from django.conf.urls import include, url

from arcutils import admin
from arcutils.drf.routers import DefaultRouter
import arcutils.cas.urls

from .views import AppView

from .locations.views import LocationViewSet, square_footage
from .pages.views import PageViewSet, slugify_name


urlpatterns = [
    # Home
    url(r'^$', AppView.as_view(template_name='base.html'), name='home'),

    # Admin
    url(r'^admin/', admin.cas_site.urls),

    # Auth
    url(r'', include(arcutils.cas.urls)),

    # API
    url(r'^_/locations/square-footage$', square_footage, name='square-footage'),
    url(r'^_/locations/square-footage/(?P<neighborhood>.+)$', square_footage,
        name='square-footage-neighborhood'),
    url(r'^_/pages/slugify_name$', slugify_name, name='slugify_name')
]


router = DefaultRouter()
router.register(r'_/locations', LocationViewSet)
router.register(r'_/pages', PageViewSet)
urlpatterns += router.urls
