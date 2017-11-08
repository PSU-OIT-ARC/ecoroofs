import pkg_resources

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from arcutils.settings import get_setting


class ModelViewSet(viewsets.ModelViewSet):

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AppView(APIView):

    app_key = settings.HOME_PAGE_APP_KEY
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def get(self, request):
        user = request.user
        initials = None
        if not user.is_anonymous():
            initials = "{}{}".format(user.first_name[0], user.last_name[0])

        dist = pkg_resources.get_distribution('psu.oit.wdt.ecoroofs')
        return Response({
            'CDN_URLS': {
                'css': get_setting('CDN_URLS.css'),
                'js': get_setting('CDN_URLS.js'),
            },
            'STATIC_PATHS': {
                'css': get_setting('STATIC_PATHS.css'),
                'js': get_setting('STATIC_PATHS.js'),
            },

            # Config that's passed through to the JavaScript app.
            'APP_CONFIG': {
                'env': settings.ENV,
                'version': dist.version,
                'baseURL': settings.STATIC_URL,
                'title': settings.PROJECT.title,
                'user': {
                    'isAuthenticated': user.is_authenticated(),
                    'username': user.username,
                    'fullName': user.get_full_name() if not user.is_anonymous() else None,
                    'isStaff': user.is_staff,
                    'isSuperuser': user.is_superuser,
                    'initials': initials
                },
                'map': settings.MAP,
            },
        })
