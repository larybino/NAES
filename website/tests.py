from pathlib import Path

from django.conf import settings
from django.template import engines
from django.test import SimpleTestCase
from django.urls import reverse


class TemplateTests(SimpleTestCase):
    def test_project_templates_compile(self):
        engine = engines["django"]
        for app in ("website", "pacients", "treatments", "documents"):
            for path in (Path(settings.BASE_DIR) / app / "templates").rglob("*.html"):
                with self.subTest(template=str(path)):
                    engine.from_string(path.read_text(encoding="utf-8"))

    def test_login_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_patient_registration_redirects_to_working_login(self):
        response = self.client.get("/pacients/cadastrar/paciente/", follow=True)
        self.assertRedirects(response, "/login/?next=/pacients/cadastrar/paciente/")
