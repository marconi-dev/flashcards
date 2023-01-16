from rest_framework.serializers import ModelSerializer

from .models import User

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username':{'required':True}
        }


    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)