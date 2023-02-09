from rest_framework import serializers


class EstudosSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    frente_imagem = serializers.ImageField(source='frente.imagem')
    frente_texto = serializers.StringRelatedField(source='frente.texto')
    verso = serializers.StringRelatedField()
