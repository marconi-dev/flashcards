from rest_framework.serializers import ModelSerializer

from .models import User

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)