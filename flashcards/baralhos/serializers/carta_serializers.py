from datetime import date

from rest_framework import serializers
from baralhos.models import Carta, Frente, Verso, Baralho


class CartaCreateSerializer(serializers.Serializer):
    frente = serializers.CharField(required=False)
    frente_img = serializers.ImageField(required=False)
    verso = serializers.CharField()
    
    def validate(self, attrs):
        if not 'frente' in attrs and not 'frente_img' in attrs:
            raise serializers.ValidationError(
                'A frente deve possuir ao menos um texto ou uma imagem'
            ) 
        return attrs


    def __set_frente_info(self, data):
        """
        Define as informações da instancia (Frente) que será 
        utilizada na carta.
        """
        frente = dict()
        
        if 'frente_img' in data:
            frente['imagem'] = data['frente_img']
        
        elif 'frente' in data.keys():
            frente['texto'] = data['frente']
        
        return frente
    
    def create(self, data):
        baralho_pk = self.context['baralho_pk']
        frente_info = self.__set_frente_info(data)

        carta = dict()
        carta['frente'] = Frente.objects.create(**frente_info)
        carta['verso'] = Verso.objects.create(texto=data['verso'])
        carta['baralho'] = Baralho.objects.get(pk=baralho_pk)
        carta['proxima_revisao'] = date.today()
        carta['tags'] = None
        return Carta.objects.create(**carta)

    def update(self, carta, data):
        carta.frente.texto = data.get('frente', carta.frente.texto)
        carta.frente.frente_img = data.get('frente_img', carta.frente.imagem) 
        carta.verso.texto = data.get('verso', carta.verso.texto)
        carta.save()
        return carta 


class CartaSerializer(serializers.ModelSerializer):
    verso = serializers.StringRelatedField()
    frente = serializers.StringRelatedField()
    imagem = serializers.ImageField(source='frente.imagem')


    class Meta:
        model = Carta
        fields = [
            'id', 'frente', 'verso', 'nivel',
            'imagem', 'proxima_revisao', 'vista'
        ]
    