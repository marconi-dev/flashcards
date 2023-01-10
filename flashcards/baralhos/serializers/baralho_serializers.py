from rest_framework import serializers
from baralhos.models import Baralho, Carta


class BaralhoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baralho
        fields = [
            'nome', 'num_cartas_nao_vistas', 
            'num_cartas_para_revisar', 'total_de_cartas'
        ]


class BaralhoSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    
    class Meta:
        model = Baralho
        fields = [
            'usuario', 'id', 'nome', 
            'num_cartas_nao_vistas', 
            'num_cartas_para_revisar'
        ]
        read_only_fields = [ 
            'num_cartas_nao_vistas',
            'num_cartas_para_revisar'
        ]
