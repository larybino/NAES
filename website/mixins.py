from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


class BaseLoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class GroupRequiredMixin(BaseLoginMixin, UserPassesTestMixin):
    """Require the current user to belong to one or more groups.

    Set `group_required` to a string or iterable of group names on the view.
    Example:
        group_required = ('admins', 'managers')
    """

    group_required = None

    def test_func(self):
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return False

        if not self.group_required:
            return True

        required = self.group_required
        if isinstance(required, str):
            required = (required,)

        user_groups = {g.name for g in user.groups.all()}
        return bool(user_groups.intersection(set(required)))


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.is_authenticated:
            return form

        for field in form.fields.values():
            queryset = getattr(field, "queryset", None)
            if queryset is None:
                continue

            related_user_field = self._get_user_field_name(queryset.model)
            if related_user_field:
                field.queryset = queryset.filter(**{related_user_field: self.request.user})

        return form

    def form_valid(self, form):
        user_field = self._get_user_field_name(form.instance.__class__)
        if user_field and not getattr(form.instance, user_field, None):
            setattr(form.instance, user_field, self.request.user)

        return super().form_valid(form)
