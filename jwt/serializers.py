from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class ActorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("name", "year", "genre", "actor")

class CommitMoviesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommitMovie
        fields = ("id", "title", "movie", "author")
        read_only_fields = ["author"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "detail": "User does not exist"
            })

        auth_user = authenticate(username=username, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "Username or password is invalid"
            })

        
        attrs["user"] = auth_user
        return attrs    