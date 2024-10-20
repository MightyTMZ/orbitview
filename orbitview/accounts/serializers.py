from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id',
            'user_name',
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'username',
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
            
        ]


