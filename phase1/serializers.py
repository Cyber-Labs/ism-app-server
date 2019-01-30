from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'