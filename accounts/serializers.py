from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer

try:

    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email

except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # username= None
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    age = serializers.IntegerField(required=True)
    sex = serializers.IntegerField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email',''),
            'name': self.validated_data.get('name', ''),
            'age' : self.validated_data.get('age', ''),
            'sex' : self.validated_data.get('sex', ''),
        }

    def save(self, request):
        
        # super(CustomRegisterSerializer, self).get_cleaned_data()
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()

        user.age=self.cleaned_data.get('age')
        user.sex=self.cleaned_data.get('sex')
        # user.email = self.cleaned_data.get('email')
        user.name = self.cleaned_data.get('name')
        # user.username= None

        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        self.custom_signup(request, user)
        user.save()
        return user

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name','age','sex')
        read_only_fields = ('email',)      

class CustomLoginSerializer(LoginSerializer):
    username = None

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'name','email','age','sex')
