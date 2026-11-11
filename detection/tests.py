from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json

from detection.models import MessageAnalysis, Feedback
from ml_engine.preprocessing import clean_text, extract_trigger_words
from ml_engine.predict import predict_message


class CyberShieldDetectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )

    def test_text_preprocessing(self):
        """Tests that URLs, mentions, emojis, and repeated characters are cleaned."""
        raw = "Check this out https://malicious.com @someone you are sooooo bad 😡!!!"
        cleaned = clean_text(raw)
        self.assertNotIn("https://malicious.com", cleaned)
        self.assertNotIn("@someone", cleaned)
        self.assertIn("angry", cleaned)  # Emoji decoded

    def test_trigger_words_extraction(self):
        """Tests keyword trigger detection for explainability."""
        text = "I will find and kill you, you loser."
        triggers = extract_trigger_words(text)
        self.assertIn("kill", triggers)
        self.assertIn("loser", triggers)

    def test_ml_prediction_service(self):
        """Tests machine learning prediction output structure."""
        safe_res = predict_message("This is a wonderful and encouraging project, thank you!")
        self.assertTrue(safe_res['success'])
        self.assertEqual(safe_res['risk_level'], 'Safe')
        self.assertIn('confidence_score', safe_res)
        self.assertIn('recommendations', safe_res)

        threat_res = predict_message("I will find where you live and kill you tonight.")
        self.assertTrue(threat_res['success'])
        self.assertEqual(threat_res['risk_level'], 'High-Risk Content')
        self.assertEqual(threat_res['predicted_category'], 'Threatening Language')

    def test_home_page_renders(self):
        """Tests landing page loads with status 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creating a")
        self.assertContains(response, "CyberShield")

    def test_detection_view_post(self):
        """Tests submitting a message via web detection form."""
        response = self.client.post(reverse('detection'), {
            'message': 'You are an absolute loser, leave this platform now.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MessageAnalysis.objects.count(), 1)
        analysis = MessageAnalysis.objects.first()
        self.assertIn('loser', analysis.original_text)

    def test_api_analyze_json(self):
        """Tests the REST API /api/analyze/ endpoint."""
        payload = json.dumps({'message': 'Have a blessed day everyone!'})
        response = self.client.post(
            reverse('api_analyze'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['risk_level'], 'Safe')

    def test_feedback_submission(self):
        """Tests user feedback recording."""
        analysis = MessageAnalysis.objects.create(
            original_text="Test message",
            predicted_category="Normal / Safe",
            confidence_score=90.0,
            risk_level="Safe"
        )
        response = self.client.post(reverse('submit_feedback'), {
            'analysis_id': analysis.id,
            'feedback_type': 'accurate',
            'comments': 'Great prediction'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.first().analysis, analysis)

    def test_dashboard_view(self):
        """Tests moderation dashboard loads successfully."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('analytics', response.context)
        self.assertIn('page_obj', response.context)
