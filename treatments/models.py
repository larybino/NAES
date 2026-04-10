from django.db import models
from pacients.models import Patient

class TreatmentPlan(models.Model):
    STATUS_CHOICES = [
        ("draft", "Em elaboração"),
        ("approved", "Aprovado"),
        ("in_progress", "Em andamento"),
        ("completed", "Concluído"),
        ("cancelled", "Cancelado"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="treatment_plans",
        verbose_name="Paciente"
    )
    created_at = models.DateField("Data de Criação", auto_now_add=True)
    total_value = models.DecimalField("Valor Total", max_digits=10, decimal_places=2, default=0)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="draft")

    def approve(self):
        self.status = "approved"
        self.save()

    def cancel(self):
        self.status = "cancelled"
        self.save()

    def __str__(self):
        return f"Plano #{self.pk} — {self.patient.name} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Plano de Tratamento"
        verbose_name_plural = "Planos de Tratamento"


class PlanItem(models.Model):
    treatment_plan = models.ForeignKey(
        TreatmentPlan, on_delete=models.CASCADE, related_name="items",
        verbose_name="Plano de Tratamento"
    )
    tooth = models.CharField("Dente", max_length=10)
    procedure = models.CharField("Procedimento", max_length=200)
    value = models.DecimalField("Valor", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Dente {self.tooth} — {self.procedure}"

    class Meta:
        verbose_name = "Item do Plano"
        verbose_name_plural = "Itens do Plano"


class TreatmentPerformed(models.Model):
    PAYMENT_CHOICES = [
        ("pix", "PIX"),
        ("cash", "Dinheiro"),
        ("credit", "Cartão de Crédito"),
        ("debit", "Cartão de Débito"),
        ("installment", "Parcelado"),
    ]

    treatment_plan = models.ForeignKey(
        TreatmentPlan, on_delete=models.CASCADE, related_name="performed_treatments",
        verbose_name="Plano de Tratamento"
    )
    date = models.DateField("Data")
    tooth = models.CharField("Dente", max_length=10)
    procedure_history = models.TextField("Histórico do Procedimento")
    value = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        "Forma de Pagamento", max_length=20, choices=PAYMENT_CHOICES, blank=True
    )

    def __str__(self):
        return f"{self.date} — Dente {self.tooth} — {self.procedure_history[:40]}"

    class Meta:
        verbose_name = "Tratamento Realizado"
        verbose_name_plural = "Tratamentos Realizados"
        ordering = ["-date"]
