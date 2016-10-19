from rest_framework import serializers

from ..serializers import ModelSerializer
from ..neighborhoods.models import Neighborhood

from .models import *  # noqa


class PointSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'x': instance.x,
            'y': instance.y,
            'z': instance.z,
            'srid': instance.srid,
        }


class BuildingUseSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingUse


class NeighborhoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'slug')


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor


class WatershedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watershed


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        exclude = ('point',)

    point_obscured = PointSerializer()
    building_use = BuildingUseSerializer()
    neighborhood = NeighborhoodSerializer()
    watershed = WatershedSerializer()
    contractor = ContractorSerializer()


class PrivilegedLocationSerializer(LocationSerializer):

    """For users that have privileged access (staff, superusers).

    This includes non-obscured location data such as the actual
    coordinates and addresses of residential ecoroofs.

    """

    point = PointSerializer()
