from django import forms

from .models import Patient


def somente_digitos(valor):
    return "".join(caractere for caractere in valor if caractere.isdigit())


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

    def clean_cpf(self):
        return somente_digitos(self.cleaned_data["cpf"])

    def clean_postal_code(self):
        return somente_digitos(self.cleaned_data["postal_code"])

    def clean_phone(self):
        return somente_digitos(self.cleaned_data["phone"])

    def clean_mobile(self):
        return somente_digitos(self.cleaned_data["mobile"])

    def clean_whatsapp(self):
        return somente_digitos(self.cleaned_data["whatsapp"])

    def clean_referral_phone(self):
        return somente_digitos(self.cleaned_data["referral_phone"])