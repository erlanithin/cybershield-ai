from django.test import TestCase, Client
from django.urls import reverse
from reports.models import CyberbullyingReport


class ReportsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_report_creation(self):
        response = self.client.post(reverse('report_create'), {
            'title': 'Test Harassment Incident',
            'platform': 'Instagram',
            'category': 'Harassment',
            'offensive_message': 'You are a total loser',
            'description': 'Repeated offensive messages sent to profile'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CyberbullyingReport.objects.count(), 1)
        report = CyberbullyingReport.objects.first()
        self.assertEqual(report.title, 'Test Harassment Incident')
        self.assertEqual(report.status, 'Pending')

    def test_report_list_view(self):
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cyberbullying Incident Reports")
