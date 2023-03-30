from rest_framework.serializers import ModelSerializer

from basic_info.models import Nation, Province, City



class NationSerializer(ModelSerializer):

    class Meta:
        model=Nation
        fields='__all__'


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'