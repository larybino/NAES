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


    def test_cb02_empty_optional_fields_reach_database(self):
        optional = (
            "rg", "issuing_agency", "address", "address_number", "neighborhood",
            "city", "postal_code", "referral", "referral_phone",
        )
        data = {**self.data, **dict.fromkeys(optional, "")}
        with self.trace_flow() as trace:
            response = self.client.post(self.url, data)
            form = self.assert_success_flow(trace, response)
        patient = Patient.objects.get()
        for field in optional:
            with self.subTest(field=field):
                self.assertEqual(form.cleaned_data[field], "")
                self.assertEqual(getattr(patient, field), "")

    def test_cb02_second_patient_with_empty_optional_fields_can_be_saved(self):
        optional = (
            "rg", "issuing_agency", "address", "address_number", "neighborhood",
            "city", "postal_code", "referral", "referral_phone",
        )
        first_data = {**self.data, **dict.fromkeys(optional, "")}
        Patient.objects.create(**{**first_data, "user": self.user})
        data = {**first_data, "cpf": "111.444.777-35"}
        with self.trace_flow() as trace:
            response = self.client.post(self.url, data)
            self.assertEqual(
                response.status_code, 302,
                "Opcionais vazios bloquearam o cadastro: "
                f"{response.context['form'].errors if response.context else ''}",
            )
            self.assert_success_flow(trace, response)
        self.assertEqual(Patient.objects.count(), 2)
        patient = Patient.objects.get(cpf=data["cpf"])
        for field in optional:
            with self.subTest(field=field):
                self.assertEqual(getattr(patient, field), "")

    def test_cb03_each_required_field_blocks_save_when_empty(self):
        for field in ("name", "birth_date", "cpf", "phone", "mobile", "whatsapp", "email"):
            with self.subTest(field=field), self.trace_flow() as trace:
                response = self.client.post(self.url, {**self.data, field: ""})
                self.assert_rejected_flow(trace, response, field, "required")
                self.assertFalse(Patient.objects.exists())

    def assert_invalid_input_not_saved(self, field, value):
        with self.trace_flow() as trace:
            response = self.client.post(self.url, {**self.data, field: value})
            self.assertFalse(
                Patient.objects.exists(),
                f"O cadastro foi salvo com {field} inválido: {value!r}.",
            )
            self.assert_rejected_flow(trace, response, field)

    def test_cb04_incomplete_cpf_is_rejected(self):
        self.assert_invalid_input_not_saved("cpf", "123.456.789-0")

    def test_cb05_cpf_with_letters_is_rejected(self):
        self.assert_invalid_input_not_saved("cpf", "ABC.DEF.GHI-JK")

    def test_cb06_incomplete_postal_code_is_rejected(self):
        self.assert_invalid_input_not_saved("postal_code", "12345-67")

    def test_cb07_email_without_at_sign_selects_invalid_branch(self):
        with self.trace_flow() as trace:
            response = self.client.post(self.url, {**self.data, "email": "paciente.exemplo.com"})
            self.assert_rejected_flow(trace, response, "email", "invalid")
        self.assertFalse(Patient.objects.exists())

    def test_cb08_user_is_assigned_before_real_model_save(self):
        observed = []
        original_save = Patient.save

        def observe_save(instance, *args, **kwargs):
            observed.append((instance.user_id, instance.name, instance.pk))
            return original_save(instance, *args, **kwargs)

        with self.trace_flow() as trace, patch.object(
            Patient, "save", autospec=True, side_effect=observe_save
        ) as model_save:
            response = self.client.post(self.url, self.data)
            self.assert_success_flow(trace, response)
            model_save.assert_called_once()
        self.assertEqual(observed, [(self.user.pk, "Paciente Exemplo", None)])
        self.assertEqual(Patient.objects.get().user_id, self.user.pk)

    def test_cb09_duplicate_cpf_blocks_save(self):
        Patient.objects.create(**{**self.data, "user": self.user})
        with self.trace_flow() as trace:
            response = self.client.post(self.url, {**self.data, "rg": "987654321"})
            self.assert_rejected_flow(trace, response, "cpf", "unique")
        self.assertEqual(Patient.objects.count(), 1)

    def test_cb10_save_failure_propagates_without_success_redirect(self):
        with self.trace_flow() as trace, patch.object(
            Patient, "save", autospec=True, side_effect=DatabaseError("falha controlada")
        ) as model_save:
            with self.assertRaisesMessage(DatabaseError, "falha controlada"):
                self.client.post(self.url, self.data)
            trace.valid.assert_called_once()
            trace.save.assert_called_once()
            model_save.assert_called_once()
            trace.invalid.assert_not_called()
            trace.success_url.assert_not_called()
            view, form = trace.valid.call_args.args
            self.assertEqual(form.instance.user, self.user)
            self.assertIsNone(view.object)
        self.assertFalse(Patient.objects.exists())

    def test_cb11_controlled_save_result_becomes_view_object_before_redirect(self):
        saved_result = Patient(pk=123, name="Resultado controlado", user=self.user)
        with self.trace_flow() as trace:
            trace.save.side_effect = None
            trace.save.return_value = saved_result
            response = self.client.post(self.url, self.data)
            trace.save.assert_called_once()
            trace.valid.assert_called_once()
            trace.invalid.assert_not_called()
            view = trace.valid.call_args.args[0]
            self.assertIs(view.object, saved_result)
            trace.success_url.assert_called_once_with(view)
            self.assertRedirects(
                response, reverse("listar_pacientes"), fetch_redirect_response=False
            )
        self.assertFalse(Patient.objects.exists())

    def test_anonymous_post_never_reaches_validation_or_save(self):
        self.client.logout()
        with self.trace_flow() as trace:
            response = self.client.post(self.url, self.data)
            trace.validate.assert_not_called()
            trace.valid.assert_not_called()
            trace.invalid.assert_not_called()
            trace.save.assert_not_called()
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.url}", fetch_redirect_response=False
        )
        self.assertFalse(Patient.objects.exists())