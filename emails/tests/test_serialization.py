import email
from unittest import TestCase

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

from emails.serialization import email_to_dict, dict_to_email


class EmailSerializationTests(TestCase):

    def test_email_message_to_dict(self):
        payload = EmailMessage(
            subject='Test email',
            body='This is a test email.',
            from_email='test@example.com',
            to=['test@example.com']
        )
        result = email_to_dict(payload)
        self.assertEqual(result['subject'], 'Test email')
        self.assertEqual(result['body'], 'This is a test email.')
        self.assertEqual(result['from_email'], 'test@example.com')
        self.assertEqual(result['to'], ['test@example.com'])

    def test_email_multi_alternatives_to_dict(self):
        message = EmailMultiAlternatives(
            subject='Test email',
            body='This is a test email.',
            from_email='test@example.com',
            to=['test@example.com']
        )
        message.attach_alternative(
            '<p>This is a test email.</p>',
            'text/html'
        )
        result = email_to_dict(message)
        self.assertEqual(result['subject'], message.subject)
        self.assertEqual(result['body'], message.body)
        self.assertEqual(result['from_email'], message.from_email)
        self.assertEqual(result['to'], message.to)
        self.assertEqual(result['alternatives'], message.alternatives)

    def test_email_dict_to_dict(self):
        payload = {
            'subject': 'Test email',
            'body': 'This is a test email.',
            'from_email': 'test@example.com'
        }
        result = email_to_dict(payload)
        self.assertEqual(result, payload)

    def test_email_to_dict_invalid_type(self):
        with self.assertRaises(ValueError):
            email_to_dict('invalid')

        with self.assertRaises(ValueError):
            email_to_dict(email.message.Message())

    def test_dict_to_email(self):
        payload = {
            'subject': 'Test email',
            'body': 'This is a test email.',
            'from_email': 'test@example.com'
        }
        result = dict_to_email(payload)
        self.assertTrue(isinstance(result, EmailMessage))
        self.assertEqual(result.subject, payload['subject'])
        self.assertEqual(result.body, payload['body'])
        self.assertEqual(result.from_email, payload['from_email'])

    def test_dict_to_email_with_alternatives(self):
        payload = {
            'subject': 'Test email',
            'body': 'This is a test email.',
            'from_email': 'test@example.com',
            'alternatives': [('<p>This is a test email.</p>', 'text/html')]
        }
        result = dict_to_email(payload)
        self.assertTrue(isinstance(result, EmailMultiAlternatives))
        self.assertEqual(result.subject, payload['subject'])
        self.assertEqual(result.body, payload['body'])
        self.assertEqual(result.from_email, payload['from_email'])
        self.assertEqual(result.alternatives, payload['alternatives'])

    def test_dict_to_email_empty_dict(self):
        payload = {}
        result = dict_to_email(payload)
        self.assertEqual(result.subject, '')
        self.assertEqual(result.body, '')
        self.assertEqual(result.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(result.to, [])
        self.assertEqual(result.bcc, [])
        self.assertEqual(result.attachments, [])
        self.assertEqual(result.extra_headers, {})
        self.assertEqual(result.cc, [])
        self.assertEqual(result.reply_to, [])
