from django.db.models import Sum
from django.contrib.postgres.search import SearchQuery, SearchVector

from rest_framework.decorators import api_view, list_route
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from ..views import ModelViewSet
from .models import Location, BuildingUse
from .serializers import (LocationSerializer,
                          PrivilegedLocationSerializer,
                          BuildingUseSerializer)


class LocationViewSet(ModelViewSet):

    queryset = Location.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user and (user.is_staff or user.is_superuser):
            return PrivilegedLocationSerializer
        return LocationSerializer

    @list_route()
    def search(self, request):
        # Search
        q = self.queryset
        term = request.query_params.get('q', '').strip()
        if term:
            search_query = SearchQuery(term)
            q = q.annotate(search=SearchVector('name', 'address_obscured'))
            q = q.filter(search=search_query)

        # Filters
        usage = request.query_params.get("usage", '').strip()
        if usage:
            q = q.filter(building_use=usage)

        depth_min = request.query_params.get("depth_min", '').strip()
        if depth_min:
            q = q.filter(depth_min__gte=depth_min)

        depth_max = request.query_params.get("depth_max", '').strip()
        if depth_max:
            q = q.filter(depth_max__lte=depth_max)

        year_built_min = request.query_params.get("year_built_min", '').strip()
        if year_built_min:
            q = q.filter(year_built__gte=year_built_min)

        year_built_max = request.query_params.get("year_built_max", '').strip()
        if year_built_max:
            q = q.filter(year_built__lte=year_built_max)

        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)


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


class BuildingUseListView(ListAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = BuildingUse.objects.all()
    serializer_class = BuildingUseSerializer
