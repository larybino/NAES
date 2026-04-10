from django.db import models

class Patient (models.Model):
    name = models.CharField("Nome", max_length=100)
    birth_date = models.DateField("Data de Nascimento")
    cpf = models.CharField("CPF", max_length=14, unique=True)
    rg = models.CharField("RG", max_length=12, unique=True, blank=True)
    issuing_agency = models.CharField("Órgão Expedidor", max_length=20, blank=True)
    address = models.CharField("Endereço", max_length=200, blank=True)
    address_number = models.CharField("Número", max_length=10, blank=True)
    neighborhood = models.CharField("Bairro", max_length=50, blank=True)
    city = models.CharField("Cidade", max_length=50, blank=True)
    postal_code = models.CharField("CEP", max_length=10, blank=True)
    phone = models.CharField("Telefone", max_length=15)
    mobile = models.CharField("Celular", max_length=15)
    whatsapp = models.CharField("WhatsApp", max_length=15)
    email = models.EmailField("E-mail")
    referral = models.TextField("Indicação", blank=True)
    referral_phone = models.CharField("Telefone da Indicação", max_length=15, blank=True)

    def __str__(self):
        return self.name
    
class Anamnese(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, verbose_name="Paciente")
    brushings_per_day = models.PositiveSmallIntegerField("Escovações por dia", default=0)
    guided_brushing = models.BooleanField("Escovação orientada", default=False)
    uses_floss = models.BooleanField("Usa fio dental", default=False)
    floss_per_day = models.PositiveSmallIntegerField("Fio dental por dia", default=0)
    gum_inflammation = models.BooleanField("Gengiva inflama/sangra", default=False)
    temperature_sensitivity = models.BooleanField("Sensibilidade à temperatura", default=False)
    sweet_sensitivity = models.BooleanField("Sensibilidade ao doce", default=False)
    tooth_mobility = models.BooleanField("Mobilidade dentária", default=False)
    tmj_pain = models.BooleanField("Dor na ATM", default=False)
    jaw_clicking = models.BooleanField("Estalos na mandíbula", default=False)
    bruxism = models.BooleanField("Bruxismo", default=False)
    nasal_breathing = models.BooleanField("Respira pelo nariz", default=False)
    high_sugar_intake = models.BooleanField("Ingere muito doce", default=False)
    coffee_soda_habit = models.BooleanField("Hábito de café/refrigerante", default=False)
    last_dental_visit = models.DateField("Última consulta odontológica", null=True, blank=True)
    completed_last_treatment = models.BooleanField("Completou o último tratamento?", default=False)   
    under_medical_treatment = models.BooleanField("Em tratamento médico?", default=False)
    preexisting_conditions = models.TextField("Doenças preexistentes", blank=True)
    uses_medication = models.BooleanField("Usa medicamentos?", default=False)
    medications = models.TextField("Quais medicamentos?", blank=True)
    drug_allergy = models.BooleanField("Alergia a medicamentos?", default=False)
    allergy_description = models.CharField("Qual alergia?", max_length=200, blank=True)
    pregnant = models.BooleanField("Gestante?", default=False)
    excessive_bleeding = models.BooleanField("Sangra muito?", default=False)
    slow_healing = models.BooleanField("Feridas cicatrizam devagar?", default=False)
    digestion_issues = models.BooleanField("Dificuldade de digestão?", default=False)
    liver_kidney_problems = models.BooleanField("Problemas no fígado/rins?", default=False)
    smokes_or_drugs = models.BooleanField("Fuma ou usa drogas?", default=False)
    additional_info = models.TextField("Informações adicionais", blank=True)

    def __str__(self):
        return f"Anamnese de {self.patient.name}"