from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(password=password, **validated_data)
        user.set_password(password)
        user.save(update_fields=['password'])
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email,
                                password=password
            )
            if not user:
                raise serializers.ValidationError('User not found')
            if not user.is_active:
                raise serializers.ValidationError('User is not active')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include both email and password.')

    class Meta:
        model = User
        fields = ('email', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    post_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'avatar', 'bio', 'created_at', 'updated_at',
            'post_count', 'comment_count'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_post_count(self, obj):
        try:
            return obj.posts.count()
        except AttributeError:
            return 0

    def get_comment_count(self, obj):
        try:
            return obj.comments.count()
        except AttributeError:
            return 0

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'avatar', 'bio'
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirmation = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Wrong password')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password': 'Passwords do not match.'}
            )
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


