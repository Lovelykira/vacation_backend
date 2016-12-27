from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import VacationRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'password', 'first_name', 'last_name', 'email', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class VacationRequestSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True)

    class Meta:
        model = VacationRequest
        fields = ('user', 'start_date', 'end_date', 'comment', 'status')

    # def create(self, request):
    #     print(request)
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         VacationRequest.objects.create_user(**serializer.validated_data)
    #
    #         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    #     return JSONResponse(serializer.errors, status=400)