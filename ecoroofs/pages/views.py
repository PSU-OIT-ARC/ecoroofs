from django.utils.text import slugify

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..views import ModelViewSet
from .models import Page
from .serializers import PageSerializer


class PageViewSet(ModelViewSet):

    lookup_field = 'slug'
    queryset = Page.objects.filter(published=True)
    serializer_class = PageSerializer


@api_view()
def slugify_name(request):
    page_name = request.GET.get('name', None)
    slug = slugify(page_name) if page_name else None

    return Response({
        'slug': slug,
    })
