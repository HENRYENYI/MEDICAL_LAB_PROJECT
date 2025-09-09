from django.db import models
from django.conf import settings
from tests.models import LabTest
from consultation.models import ConsultationSpecialty

class AIConsultation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # For anonymous users
    question = models.TextField()
    ai_response = models.TextField()
    suggested_tests = models.ManyToManyField(LabTest, blank=True)
    suggested_consultations = models.ManyToManyField(ConsultationSpecialty, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_info = self.user.username if self.user else f"Anonymous ({self.session_id})"
        return f"AI Consultation - {user_info} - {self.created_at.strftime('%Y-%m-%d')}"