from django.db import models

class Patient (models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=12, unique=True, blank=True)
    issuing_agency = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    address_number = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15)
    email = models.EmailField()
    referral = models.TextField(blank=True)
    referral_phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name
    
class Anamnese(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    brushings_per_day = models.PositiveSmallIntegerField(default=0)
    guided_brushing = models.BooleanField(default=False)
    uses_floss = models.BooleanField(default=False)
    floss_per_day = models.PositiveSmallIntegerField(default=0)
    gum_inflammation = models.BooleanField(default=False)
    temperature_sensitivity = models.BooleanField(default=False)
    sweet_sensitivity = models.BooleanField(default=False)
    tooth_mobility = models.BooleanField(default=False)
    tmj_pain = models.BooleanField(default=False)
    jaw_clicking = models.BooleanField(default=False)
    bruxism = models.BooleanField(default=False)
    nasal_breathing = models.BooleanField(default=False)
    high_sugar_intake = models.BooleanField(default=False)
    coffee_soda_habit = models.BooleanField(default=False)
    last_dental_visit = models.DateField(null=True, blank=True)
    completed_last_treatment = models.BooleanField(default=False)   
    under_medical_treatment = models.BooleanField(default=False)
    preexisting_conditions = models.TextField(blank=True)
    uses_medication = models.BooleanField(default=False)
    medications = models.TextField(blank=True)
    drug_allergy = models.BooleanField(default=False)
    allergy_description = models.CharField(max_length=200, blank=True)
    pregnant = models.BooleanField(default=False)
    excessive_bleeding = models.BooleanField(default=False)
    slow_healing = models.BooleanField(default=False)
    digestion_issues = models.BooleanField(default=False)
    liver_kidney_problems = models.BooleanField(default=False)
    smokes_or_drugs = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"Anamnese de {self.patient.name}"