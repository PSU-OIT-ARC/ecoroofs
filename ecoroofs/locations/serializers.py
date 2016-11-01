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


class ConstructionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConstructionType
        fields = '__all__'


class ConfidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Confidence
        fields = '__all__'


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        exclude = ('point', 'address')

    point_obscured = PointSerializer()
    building_use = BuildingUseSerializer()
    neighborhood = NeighborhoodSerializer()
    watershed = WatershedSerializer()
    contractor = ContractorSerializer()
    depth = serializers.SerializerMethodField()
    construction_type = ConstructionTypeSerializer()
    confidence = ConfidenceSerializer()

    def get_depth(self, instance):
        """Format depth field as a string.

        If there's *only* a min depth or a max depth *or* if the min and
        max depths are the same, return that value as a string.

        If there's both a min and a max, return a string like ``m - n``.

        In any case, depth values will only include up to two decimal
        digits; insignificant trailing zeroes in the decimal part will
        be removed (e.g., 3.0 becomes "3" and 3.10 becomes "3.1").

        """
        def convert(v):
            if v is None:
                return None
            v = '{v:.2f}'.format(v=v)
            v = v.rstrip('0').rstrip('.')
            return v

        depth_min = convert(instance.depth_min)
        depth_max = convert(instance.depth_max)

        if depth_min and depth_max and depth_min != depth_max:
            depth = '{m} - {n}'.format(m=depth_min, n=depth_max)
        elif depth_min:
            depth = depth_min
        elif depth_max:
            depth = depth_max
        else:
            depth = None

        return depth


class PrivilegedLocationSerializer(LocationSerializer):

    """For users that have privileged access (staff, superusers).

    This includes non-obscured location data such as the actual
    coordinates and addresses of residential ecoroofs.

    """

    point = PointSerializer()
