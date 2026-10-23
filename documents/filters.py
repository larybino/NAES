import django_filters

from pacients.models import Patient

from .models import Contract, TermsOfService


def patient_queryset(request):
    if request is None or not request.user.is_authenticated:
        return Patient.objects.none()
    return Patient.objects.filter(user=request.user)


class TermsOfServiceFilter(django_filters.FilterSet):
    patient = django_filters.ModelChoiceFilter(queryset=patient_queryset, label="Paciente")
    signature_date = django_filters.DateFromToRangeFilter(
        label="Assinado entre",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )
    location = django_filters.CharFilter(lookup_expr="icontains", label="Local contém")
    accepts_plan = django_filters.BooleanFilter(label="Aceita o plano")

    class Meta:
        model = TermsOfService
        fields = {
            "patient": ["exact"],
            "signature_date": ["exact"],
            "location": ["icontains"],
            "accepts_plan": ["exact"],
        }


class ContractFilter(django_filters.FilterSet):
    patient = django_filters.ModelChoiceFilter(queryset=patient_queryset, label="Paciente")
    signature_date = django_filters.DateFromToRangeFilter(
        label="Assinado entre",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )
    location = django_filters.CharFilter(lookup_expr="icontains", label="Local contém")

    class Meta:
        model = Contract
        fields = {
            "patient": ["exact"],
            "signature_date": ["exact"],
            "location": ["icontains"],
        }