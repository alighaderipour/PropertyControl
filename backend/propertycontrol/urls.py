# backend/propertycontrol/urls.py

from django.urls import path
from . import views
from .views import DepartmentListCreateView, DepartmentDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    # Auth
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.profile_view, name='profile'),

    # Dashboard
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),

    # Departments
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list'),

    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),

    # Properties
    path('properties/', views.PropertyListCreateView.as_view(), name='property-list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('properties/<int:pk>/transfer/', views.property_transfer_view, name='property-transfer'),  # ✅ New route


    # Transfers
    path('transfers/', views.PropertyTransferListCreateView.as_view(), name='transfer-list'),

    # Admin
    path('admin/users/', views.UserListCreateView.as_view(), name='user-list'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
