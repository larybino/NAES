from django.db import models

from pacients.models import Patient

class TermsOfService(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="attendance_term"
    )
    signature_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100)
    accepts_plan = models.BooleanField(default=False)
    aware_of_changes = models.BooleanField(default=False)
    aware_of_withdrawal = models.BooleanField(default=False)
    authorizes_prosthesis = models.BooleanField(default=False)
    declares_truthfulness = models.BooleanField(default=False)
    patient_signature = models.CharField(max_length=200)

    def sign(self):
        from django.utils import timezone
        self.signature_date = timezone.now().date()
        self.save()

    def __str__(self):
        return f"Termo de Atendimento — {self.patient.name}"

    class Meta:
        verbose_name = "Termo de Atendimento"
        verbose_name_plural = "Termos de Atendimento"


class Contract(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="contract"
    )
    signature_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100)
    patient_signature = models.CharField(max_length=200, blank=True)
    clinic_signature = models.CharField(max_length=200, blank=True)
    witness1_signature = models.CharField(max_length=200, blank=True)
    witness2_signature = models.CharField(max_length=200, blank=True)

    def sign(self):
        from django.utils import timezone
        self.signature_date = timezone.now().date()
        self.save()

    def __str__(self):
        return f"Contrato — {self.patient.name}"

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"