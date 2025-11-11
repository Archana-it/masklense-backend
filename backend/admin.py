from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FacialAnalysis, WeeklySummary


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'full_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )


@admin.register(FacialAnalysis)
class FacialAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'has_result']
    list_filter = ['created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at']
    
    def has_result(self, obj):
        return obj.analysis_result is not None
    has_result.boolean = True


@admin.register(WeeklySummary)
class WeeklySummaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'week_start', 'week_end', 'total_analyses', 'created_at']
    list_filter = ['week_start', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at']
