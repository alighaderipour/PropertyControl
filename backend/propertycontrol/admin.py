# backend/propertycontrol/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Department, Category, Property, PropertyTransfer

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # we subclass Django’s built-in so you still get password/change-form, etc.
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Extras", {
            "fields": ("role", "department", "phone"),
        }),
    )
    list_display = (
        "username", "email", "first_name", "last_name", 
        "role", "department", "is_active", "is_staff",
    )
    list_filter = ("role", "department", "is_staff", "is_superuser", "is_active")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "manager")
    list_filter  = ("manager",)
    search_fields = ("name", "code")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name", "code", "category", 
        "department", "current_department", 
        "status", "purchase_date",
    )
    list_filter  = (
        "category", "department", 
        "current_department", "status",
    )
    search_fields = (
        "name", "code", "serial_number", 
        "brand", "model",
    )
    readonly_fields = ("code",)   # code is auto-generated


@admin.register(PropertyTransfer)
class PropertyTransferAdmin(admin.ModelAdmin):
    list_display = (
        "property", "from_department", 
        "to_department", "transfer_date", 
        "transferred_by",
    )
    list_filter  = (
        "from_department", "to_department", 
        "transferred_by",
    )
    search_fields = (
        "property__name", "property__code",
    )