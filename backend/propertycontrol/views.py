# backend/propertycontrol/views.py

from rest_framework.exceptions import ValidationError
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import User, Department, Category, Property, PropertyTransfer
from .serializers import (
    UserSerializer, LoginSerializer, DepartmentSerializer,
    CategorySerializer, PropertySerializer, PropertyTransferSerializer,
    PropertyTransferCreateSerializer
)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


# --------------------
# Authentication Views
# --------------------

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"})
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    return Response(UserSerializer(request.user).data)


# --------------------
# Departments
# --------------------

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# --------------------
# Categories
# --------------------

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# --------------------
# Properties
# --------------------

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            print("🔴 Property validation error:", e.detail)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Property.objects.all()
        search = self.request.query_params.get('search', None)
        department = self.request.query_params.get('department', None)
        category = self.request.query_params.get('category', None)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )

        if department:
            queryset = queryset.filter(current_department__id=department)

        if category:
            queryset = queryset.filter(category__id=category)

        return queryset


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Property Transfer via PUT /properties/<pk>/transfer/
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def property_transfer_view(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    new_department_id = request.data.get("department")
    if not new_department_id:
        return Response({"error": "Department ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_department = Department.objects.get(pk=new_department_id)
    except Department.DoesNotExist:
        return Response({"error": "Target department does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Create the transfer record
    PropertyTransfer.objects.create(
        property=property,
        from_department=property.current_department,
        to_department=new_department,
        transferred_by=request.user
    )

    # Update property
    property.current_department = new_department
    property.save()

    return Response(PropertySerializer(property).data, status=status.HTTP_200_OK)


# --------------------
# Transfers
# --------------------

class PropertyTransferListCreateView(generics.ListCreateAPIView):
    queryset = PropertyTransfer.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyTransferCreateSerializer
        return PropertyTransferSerializer

    def get_queryset(self):
        queryset = PropertyTransfer.objects.all()
        property_id = self.request.query_params.get('property', None)

        if property_id:
            queryset = queryset.filter(property__id=property_id)

        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_transfers(request):
    limit = request.query_params.get('limit', 5)
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 5
    
    transfers = PropertyTransfer.objects.order_by('-transfer_date')[:limit]
    serializer = PropertyTransferSerializer(transfers, many=True)
    return Response(serializer.data)


# --------------------
# Dashboard
# --------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    stats = {
        'total_properties': Property.objects.count(),
        'active_properties': Property.objects.filter(status='active').count(),
        'total_departments': Department.objects.count(),
        'total_categories': Category.objects.count(),
        'recent_transfers': PropertyTransferSerializer(
            PropertyTransfer.objects.order_by('-transfer_date')[:5],
            many=True
        ).data,
        'properties_by_department': {}
    }

    for dept in Department.objects.all():
        stats['properties_by_department'][dept.name] = Property.objects.filter(
            current_department=dept
        ).count()

    return Response(stats)


# --------------------
# Admin - Users
# --------------------

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

