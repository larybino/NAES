"""Caixa branca: POST -> validação -> instância -> save -> redirect.

Os spies executam os métodos reais, exceto nas respostas controladas indicadas.
"""

from contextlib import contextmanager
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse

from .models import Patient
from .views import PatientCreateView


class PatientRegistrationWhiteBoxTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="tester")

    def setUp(self):
        self.client.force_login(self.user)
        self.url = reverse("cadastrar_paciente")
        self.data = {
            "name": "  Paciente Exemplo  ",
            "birth_date": "1995-04-23",
            "cpf": "529.982.247-25",
            "rg": "123456789",
            "issuing_agency": "SSP",
            "address": "Rua Exemplo",
            "address_number": "10",
            "neighborhood": "Centro",
            "city": "Sao Paulo",
            "postal_code": "01001-000",
            "phone": "(11) 3333-4444",
            "mobile": "(11) 99999-1111",
            "whatsapp": "(11) 99999-2222",
            "email": "paciente@example.com",
            "referral": "Indicacao de outro paciente",
            "referral_phone": "(11) 98888-3333",
        }

    @contextmanager
    def trace_flow(self):
        """Observa as decisões reais e os objetos passados entre métodos."""
        form_class = PatientCreateView().get_form_class()
        with (
            patch.object(PatientCreateView, "get_form_class", return_value=form_class),
            patch.object(
                form_class, "is_valid", autospec=True, side_effect=form_class.is_valid
            ) as validate,
            patch.object(
                form_class, "save", autospec=True, side_effect=form_class.save
            ) as save,
            patch.object(
                PatientCreateView, "form_valid", autospec=True,
                side_effect=PatientCreateView.form_valid,
            ) as valid,
            patch.object(
                PatientCreateView, "form_invalid", autospec=True,
                side_effect=PatientCreateView.form_invalid,
            ) as invalid,
            patch.object(
                PatientCreateView, "get_success_url", autospec=True,
                side_effect=PatientCreateView.get_success_url,
            ) as success_url,
        ):
            yield SimpleNamespace(
                validate=validate, save=save, valid=valid,
                invalid=invalid, success_url=success_url,
            )

    def assert_success_flow(self, trace, response):
        trace.valid.assert_called_once()
        trace.invalid.assert_not_called()
        trace.save.assert_called_once()
        view, form = trace.valid.call_args.args
        self.assertIs(trace.validate.call_args_list[0].args[0], form)
        self.assertIs(trace.save.call_args.args[0], form)
        self.assertIs(view.object, form.instance)
        self.assertEqual(form.instance.user, self.user)
        self.assertRedirects(
            response, reverse("listar_pacientes"), fetch_redirect_response=False
        )
        return form

    def assert_rejected_flow(self, trace, response, field, code=None):
        self.assertEqual(response.status_code, 200)
        trace.invalid.assert_called_once()
        trace.valid.assert_not_called()
        trace.save.assert_not_called()
        trace.success_url.assert_not_called()
        form = trace.invalid.call_args.args[1]
        self.assertIs(trace.validate.call_args_list[0].args[0], form)
        self.assertIs(response.context["form"], form)
        self.assertEqual(set(form.errors), {field})
        if code is not None:
            self.assertEqual(form.errors.as_data()[field][0].code, code)
        self.assertNotIn(field, form.cleaned_data)
        self.assertIsNone(form.instance.pk)
        return form

    def test_cb01_complete_data_reaches_cleaned_data_instance_and_database(self):
        with self.trace_flow() as trace:
            response = self.client.post(self.url, self.data)
            form = self.assert_success_flow(trace, response)
        patient = Patient.objects.get()
        expected = {**self.data, "name": "Paciente Exemplo", "birth_date": date(1995, 4, 23)}
        for field, value in expected.items():
            with self.subTest(field=field):
                self.assertEqual(form.data[field], self.data[field])
                self.assertEqual(form.cleaned_data[field], value)
                self.assertEqual(getattr(form.instance, field), value)
                self.assertEqual(getattr(patient, field), value)
        self.assertEqual(patient.user_id, self.user.pk)

