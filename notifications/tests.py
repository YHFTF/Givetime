from django.test import TestCase
from django.utils.module_loading import import_string

class ContextProcessorsTests(TestCase):
    def test_unread_notifications_import(self):
        func = import_string('notifications.context_processors.unread_notifications')
        self.assertTrue(callable(func))
