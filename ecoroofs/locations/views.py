from django.db.models import Sum
from django.contrib.postgres.search import SearchQuery, SearchVector

from rest_framework.decorators import api_view, list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from ..views import ModelViewSet
from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @list_route()
    def search(self, request):
        term = request.query_params.get('q', '').strip()
        if not term:
            raise ParseError('Missing search term (q query parameter)')
        search_query = SearchQuery(term)
        q = Location.objects.annotate(search=SearchVector('name'))
        q = q.filter(search=search_query)
        serializer = self.get_serializer(q, many=True)
        return Response({
            'matches': serializer.data,
        })


@api_view()
def square_footage(request, neighborhood=None):
    """Get location square footage.

    The total square footage of all locations is always included. If
    a neighborhood is specified, the neighborhood total will be included
    too. The structure of JSON responses is::

        {
            "total": N,
            "neighborhood": "{neighborhood}"|null,
            "neighborhood_total": N|null
        }

    """
    q = Location.objects.all()
    total = q.aggregate(total=Sum('square_footage'))['total']

    if neighborhood:
        q = q.filter(neighborhood__slug=neighborhood)
        neighborhood_total = q.aggregate(total=Sum('square_footage'))['total']
    else:
        neighborhood_total = None

    return Response({
        'total': total,
        'neighborhood': neighborhood,
        'neighborhood_total': neighborhood_total,
    })
