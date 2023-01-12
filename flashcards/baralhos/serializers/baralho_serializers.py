from rest_framework import serializers
from rest_framework import serializers

from baralhos.models.models import Baralho, Carta, Tag

class CartaRelation(serializers.ModelSerializer):
    frente = serializers.StringRelatedField()
    verso = serializers.StringRelatedField()
    

    class Meta:
        model = Carta
        fields = ['frente', 'verso', 'proxima_revisao']


class BaralhoDetailSerializer(serializers.ModelSerializer):
    cartas = CartaRelation(many=True)
    tags = serializers.StringRelatedField(many=True)
    
    
    class Meta:
        model = Baralho
        fields = [
            'nome', 'num_cartas_nao_vistas', 
            'num_cartas_para_revisar', 'total_de_cartas', 
            'tags', 'cartas'
        ]


class BaralhoSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.CharField(required=False, write_only=True)


    class Meta:
        model = Baralho
        fields = [
            'usuario', 'id', 'nome', 
            'num_cartas_nao_vistas', 
            'num_cartas_para_revisar',
            'tags'
        ]
        read_only_fields = [ 
            'num_cartas_nao_vistas',
            'num_cartas_para_revisar'
        ]

    def validate_tags(self, tags):
        try: return tags.lstrip().strip().lower().split(' ')
        except:
            raise serializers.ValidationError(
                'Tags devem ser separadas por espaço em branco'
            )
    
    def __add_tags(self, tags, baralho):
        """
        Adiciona tags à carta. Se necessário cria a tag.
        """
        for nome in tags:
            tag = Tag.objects.get_or_create(nome=nome)
            baralho.tags.add(tag[0])

    def create(self, data):
        if 'tags' in data: 
            tags = data.pop('tags')
            baralho = Baralho.objects.create(**data)
            self.__add_tags(tags, baralho)
            return baralho
        
        return Baralho.objects.create(**data) 
        
        

        