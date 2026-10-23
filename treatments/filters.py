import django_filters

from pacients.models import Patient

from .models import PlanItem, TreatmentPerformed, TreatmentPlan


def patient_queryset(request):
    if request is None or not request.user.is_authenticated:
        return Patient.objects.none()
    return Patient.objects.filter(user=request.user)


def treatment_plan_queryset(request):
    if request is None or not request.user.is_authenticated:
        return TreatmentPlan.objects.none()
    return TreatmentPlan.objects.filter(user=request.user)


class TreatmentPlanFilter(django_filters.FilterSet):
    patient = django_filters.ModelChoiceFilter(queryset=patient_queryset, label="Paciente")
    created_at = django_filters.DateFromToRangeFilter(
        label="Criado entre",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )
    total_value = django_filters.RangeFilter(label="Valor total entre")
    status = django_filters.ChoiceFilter(
        label="Status", choices=TreatmentPlan.STATUS_CHOICES
    )

    class Meta:
        model = TreatmentPlan
        fields = {
            "patient": ["exact"],
            "created_at": ["exact"],
            "total_value": ["exact"],
            "status": ["exact"],
        }


class TreatmentPerformedFilter(django_filters.FilterSet):
    treatment_plan = django_filters.ModelChoiceFilter(
        queryset=treatment_plan_queryset,
        label="Plano de tratamento",
    )
    date = django_filters.DateFromToRangeFilter(
        label="Realizado entre",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )
    value = django_filters.RangeFilter(label="Valor entre")
    payment_method = django_filters.ChoiceFilter(
        label="Forma de pagamento",
        choices=TreatmentPerformed.PAYMENT_CHOICES,
    )
    procedure_history = django_filters.CharFilter(
        lookup_expr="icontains", label="Procedimento contém"
    )

    class Meta:
        model = TreatmentPerformed
        fields = {
            "treatment_plan": ["exact"],
            "date": ["exact"],
            "value": ["exact"],
            "payment_method": ["exact"],
            "procedure_history": ["icontains"],
        }


class PlanItemFilter(django_filters.FilterSet):
    treatment_plan = django_filters.ModelChoiceFilter(
        queryset=treatment_plan_queryset,
        label="Plano de tratamento",
    )
    tooth = django_filters.CharFilter(lookup_expr="icontains", label="Dente contém")
    procedure = django_filters.CharFilter(
        lookup_expr="icontains", label="Procedimento contém"
    )
    value = django_filters.RangeFilter(label="Valor entre")

    class Meta:
        model = PlanItem
        fields = {
            "treatment_plan": ["exact"],
            "tooth": ["icontains"],
            "procedure": ["icontains"],
            "value": ["exact"],
        }