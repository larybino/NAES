from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class BaseLoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class UserOwnedObjectMixin:
    """Automatically binds and filters objects by the authenticated user when a user FK exists."""

    user_field_candidates = ("user", "owner", "created_by")

    def _get_user_field_name(self, model_class):
        field_names = {field.name for field in model_class._meta.concrete_fields}
        for field_name in self.user_field_candidates:
            if field_name in field_names:
                return field_name
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()

        user_field = self._get_user_field_name(queryset.model)
        if not user_field:
            return queryset

        return queryset.filter(**{user_field: self.request.user})

    def form_valid(self, form):
        user_field = self._get_user_field_name(form.instance.__class__)
        if user_field and not getattr(form.instance, user_field, None):
            setattr(form.instance, user_field, self.request.user)

        return super().form_valid(form)
