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
        fields = '__all__'


class NeighborhoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'slug')


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor
        fields = '__all__'


class WatershedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watershed
        fields = '__all__'


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        exclude = ('point',)

    point_obscured = PointSerializer()
    building_use = BuildingUseSerializer()
    neighborhood = NeighborhoodSerializer()
    watershed = WatershedSerializer()
    contractor = ContractorSerializer()
    depth = serializers.SerializerMethodField()

    def get_depth(self, instance):
        """
        Format depth as a string of one value or a range as needed.
        Format values to only include significant digits.
        """
        depth = None
        if instance.depth_min:
            depth = "{0:g}".format(float(instance.depth_min))
        if instance.depth_max and instance.depth_min != instance.depth_max:
            depth = "{0} - {1:g}".format(depth, float(instance.depth_max))
        return depth


class PrivilegedLocationSerializer(LocationSerializer):

    """For users that have privileged access (staff, superusers).

    This includes non-obscured location data such as the actual
    coordinates and addresses of residential ecoroofs.

    """

    point = PointSerializer()
