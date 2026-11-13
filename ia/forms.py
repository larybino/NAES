from django import forms

from .models import AIConfiguration


class AIConfigurationForm(forms.ModelForm):
    class Meta:
        model = AIConfiguration
        fields = ['name', 'provider_url', 'model', 'api_key', 'system_instructions', 'monthly_token_limit', 'is_active']
        widgets = {
            'api_key': forms.PasswordInput(render_value=True),
            'system_instructions': forms.Textarea(attrs={'rows': 6}),
        }
