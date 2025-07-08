from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Property(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('under_maintenance', 'Under Maintenance'),
        ('disposed', 'Disposed'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, editable=False)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='owned_properties'
    )

    current_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_department_properties'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    serial_number = models.CharField(max_length=100, blank=True)
    property_code = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_properties'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8].upper()
        if not self.current_department and self.department:
            self.current_department = self.department
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class PropertyTransfer(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    from_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='transfers_from'
    )
    to_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='transfers_to'
    )
    transfer_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    transferred_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiated_transfers'
    )

    def __str__(self):
        return f"{self.property.name} from {self.from_department.name} to {self.to_department.name}"
    