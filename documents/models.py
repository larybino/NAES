from django.db import models

from pacients.models import Patient

class TermsOfService(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="attendance_term",
        verbose_name="Paciente"
    )
    signature_date = models.DateField("Data da Assinatura", null=True, blank=True)
    location = models.CharField("Local", max_length=100)
    accepts_plan = models.BooleanField("Aceita o Plano?", default=False)
    aware_of_changes = models.BooleanField("Ciente das Alterações?", default=False)
    aware_of_withdrawal = models.BooleanField("Ciente da Desistência?", default=False)
    authorizes_prosthesis = models.BooleanField("Autoriza Prótese?", default=False)
    declares_truthfulness = models.BooleanField("Declara Veracidade?", default=False)
    patient_signature = models.CharField("Assinatura do Paciente", max_length=200)

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
        Patient, on_delete=models.CASCADE, related_name="contract",
        verbose_name="Paciente"
    )
    signature_date = models.DateField("Data da Assinatura", null=True, blank=True)
    location = models.CharField("Local", max_length=100)
    patient_signature = models.CharField("Assinatura do Paciente", max_length=200, blank=True)
    clinic_signature = models.CharField("Assinatura do Consultório", max_length=200, blank=True)
    witness1_signature = models.CharField("Assinatura da Testemunha 1", max_length=200, blank=True)
    witness2_signature = models.CharField("Assinatura da Testemunha 2", max_length=200, blank=True)

    def sign(self):
        from django.utils import timezone
        self.signature_date = timezone.now().date()
        self.save()

    def __str__(self):
        return f"Contrato — {self.patient.name}"

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"