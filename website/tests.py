from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from pacients.models import Patient
from pacients.views import PatientListView


class UserOwnershipTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.owner = user_model.objects.create_user(
			username="owner", password="password123"
		)
		self.other_user = user_model.objects.create_user(
			username="other", password="password123"
		)
		patient_data = {
			"name": "Paciente do proprietário",
			"birth_date": "1990-01-01",
			"cpf": "11111111111",
			"rg": "1111111",
			"phone": "41999999999",
			"mobile": "41999999998",
			"whatsapp": "41999999997",
			"email": "owner@example.com",
		}
		Patient.objects.create(user=self.owner, **patient_data)
		Patient.objects.create(
			user=self.other_user,
			**{**patient_data, "name": "Paciente de outro", "cpf": "22222222222", "rg": "2222222", "email": "other@example.com"},
		)

	def test_patient_list_only_returns_logged_in_user_records(self):
		self.client.force_login(self.owner)

		response = self.client.get("/pacients/listar/pacientes/")

		self.assertContains(response, "Paciente do proprietário")
		self.assertNotContains(response, "Paciente de outro")

	def test_pagination_tag_preserves_filters_without_duplicate_page(self):
		request = RequestFactory().get("/pacients/listar/pacientes/?name=Ana&page=1")
		rendered = Template(
			'{% load query_params %}{% query_params page=2 %}'
		).render(Context({"request": request}))

		self.assertEqual(rendered, "?name=Ana&amp;page=2")

# Create your tests here.
