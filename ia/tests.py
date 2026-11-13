from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import AIConfiguration, AIConversationMessage


class AIViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='ia-user', password='password123'
        )
        AIConfiguration.objects.create(
            api_key='test-key',
            system_instructions='Seja objetivo.',
        )

    def test_assistant_requires_login(self):
        response = self.client.get(reverse('ia_assistente'))
        self.assertEqual(response.status_code, 302)

    @patch('ia.views.chamar_ia', return_value=('Resposta **segura** <script>alert(1)</script>', 8))
    def test_assistant_sends_only_last_five_messages_and_sanitizes_markdown(self, mock_call):
        self.client.force_login(self.user)
        for index in range(6):
            AIConversationMessage.objects.create(
                user=self.user, role='user', content=f'Pergunta {index}'
            )

        response = self.client.post(
            reverse('ia_perguntar'),
            {'question': 'Pergunta atual'},
        )

        self.assertEqual(response.status_code, 200)
        sent_messages = mock_call.call_args.args[1]
        self.assertEqual(len(sent_messages), 5)
        self.assertEqual(sent_messages[-1]['content'], 'Pergunta atual')
        self.assertIn('<strong>segura</strong>', response.json()['answer_html'])
        self.assertNotIn('<script>', response.json()['answer_html'])
