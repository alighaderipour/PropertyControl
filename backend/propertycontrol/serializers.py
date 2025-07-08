from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, Department, Category, Property, PropertyTransfer
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'role', 'department', 'phone'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data['user'] = user
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(
        source='manager.get_full_name', read_only=True
    )

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'manager',
            'manager_name', 'description', 'created_at'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'description']


class PropertySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )
    department_name = serializers.CharField(
        source='department.name', read_only=True
    )
    current_department_name = serializers.CharField(
        source='current_department.name', read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True
    )

    class Meta:
        model = Property
        fields = [
            'id', 'code', 'name', 'description',
            'category', 'department', 'current_department',
            'status', 'purchase_date', 'purchase_price',
            'current_value', 'serial_number','property_code', 'brand', 'model',
            'image', 'category_name', 'department_name',
            'current_department_name', 'created_by',
            'created_by_name', 'created_at', 'updated_at',
        ]
        read_only_fields = ['code', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # auto-set the creator
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PropertyTransferSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(
        source='property.name', read_only=True
    )
    property_code = serializers.CharField(
        source='property.property_code', read_only=True
    )
    from_department_name = serializers.CharField(
        source='from_department.name', read_only=True
    )
    to_department_name = serializers.CharField(
        source='to_department.name', read_only=True
    )
    transferred_by_name = serializers.CharField(
        source='transferred_by.get_full_name', read_only=True
    )

    class Meta:
        model = PropertyTransfer
        fields = [
            'id',
            'property',
            'property_name',
            'property_code',
            'from_department',
            'from_department_name',
            'to_department',
            'to_department_name',
            'transfer_date',
            'notes',
            'transferred_by',
            'transferred_by_name'
        ]

class PropertyTransferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTransfer
        fields = ['property', 'to_department', 'notes']

    def create(self, validated_data):
        prop = validated_data['property']
        validated_data['from_department'] = prop.current_department
        validated_data['transferred_by'] = self.context['request'].user
        transfer = super().create(validated_data)
        # update the property's department
        prop.current_department = validated_data['to_department']
        prop.save()
        return transfer