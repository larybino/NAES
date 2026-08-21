from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # últimos cadastros recentes para exibir no dashboard
        from pacients.models import Patient
        from treatments.models import TreatmentPlan

        context['recent_patients'] = Patient.objects.order_by('-pk')[:5]
        context['recent_plans'] = (
            TreatmentPlan.objects.select_related('patient').order_by('-created_at')[:5]
        )
        return context


class AboutView(TemplateView):
    template_name = "website/about.html"