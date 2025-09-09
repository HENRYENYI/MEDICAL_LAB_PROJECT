from django.contrib import admin
from .models import AIConsultation

@admin.register(AIConsultation)
class AIConsultationAdmin(admin.ModelAdmin):
    list_display = ('get_user_info', 'question_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('question', 'ai_response', 'user__username')
    readonly_fields = ('created_at',)
    
    def get_user_info(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anonymous ({obj.session_id[:8]}...)"
    get_user_info.short_description = 'User'
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'