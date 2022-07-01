from rest_framework import serializers
from accounts.models import UserProfile
from django.contrib.auth import get_user_model




class RegisterSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'password']

    def get_gender(self, obj):
        data = self.context['request'].data
        return data.get("gender")

    def save(self, request):
        validated_data = self.validated_data
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_active=True
        )

        user_profile = UserProfile.objects.get_or_create(
            user = user.id,
            defaults={
                'user': user,
                'gender': self.data.get('gender'),
            }
        )
        user.profile = user_profile[0]
        user.save()

        return user


class LibrarianRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name','password']

        extra_kwargs = {
            'password':{'required':False}
        }

    def save(self, request):
        validated_data = self.validated_data
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=self.data.get("password"),
            is_active=True,
            is_staff=True
        )

        user_profile = UserProfile.objects.get_or_create(
            user = user.id,
            defaults={
                'user': user,
            }
        )
        user.profile = user_profile[0]
        user.save()
        return user


class UpdatePasswordSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

class ChangePasswordSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'new_password']

        

        