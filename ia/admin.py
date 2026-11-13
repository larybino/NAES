from django.contrib import admin

from .models import AIConfiguration, AIConversationMessage, AIRequestAudit, MonthlyQuota


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'is_active', 'monthly_token_limit', 'updated_at')


@admin.register(AIRequestAudit)
class AIRequestAuditAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'tokens_used', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(MonthlyQuota)
class MonthlyQuotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'tokens_used', 'token_limit')


@admin.register(AIConversationMessage)
class AIConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    readonly_fields = ('created_at',)
