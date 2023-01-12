from rest_framework import serializers
from baralhos.models.models import Baralho

class SimpleBaralhoSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Baralho
        fields = ['id', 'nome', 'tags']
    

class DetailBaralhoSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    usuario = serializers.StringRelatedField(
        source='usuario.username'
    )
    class Meta:
        model = Baralho
        fields = [
            'id', 'nome', 'tags', 
            'total_de_cartas', 'usuario'
        ]
    