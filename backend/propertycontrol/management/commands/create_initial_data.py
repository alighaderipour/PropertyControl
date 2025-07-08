# backend/propertycontrol/management/commands/create_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from propertycontrol.models import Department, Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **options):
        # ایجاد Superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@company.com',
                password='admin123',
                first_name='مدیر',
                last_name='سیستم',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # ایجاد کاربر عادی
        if not User.objects.filter(username='user1').exists():
            regular_user = User.objects.create_user(
                username='user1',
                email='user1@company.com',
                password='user123',
                first_name='کاربر',
                last_name='تست',
                role='user'
            )
            self.stdout.write(self.style.SUCCESS('Regular user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Regular user already exists'))

        # ایجاد بخش‌های نمونه
        departments = [
            {'name': 'فناوری اطلاعات', 'code': 'IT'},
            {'name': 'منابع انسانی', 'code': 'HR'},
            {'name': 'مالی', 'code': 'FIN'},
            {'name': 'عملیات', 'code': 'OPS'},
        ]
        
        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            if created:
                self.stdout.write(f'Department {dept_data["name"]} created')
            else:
                self.stdout.write(f'Department {dept_data["name"]} already exists')

        # ایجاد دسته‌بندی‌های نمونه با code
        categories = [
            {'name': 'کامپیوتر و لپ‌تاپ', 'code': 'COMP'},
            {'name': 'پرینتر و اسکنر', 'code': 'PRINT'},
            {'name': 'مبلمان اداری', 'code': 'FURN'},
            {'name': 'تجهیزات شبکه', 'code': 'NET'},
            {'name': 'لوازم جانبی', 'code': 'ACC'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                code=cat_data['code'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Category {cat_data["name"]} created')
            else:
                self.stdout.write(f'Category {cat_data["name"]} already exists')

        self.stdout.write(self.style.SUCCESS('Initial data created successfully!'))
