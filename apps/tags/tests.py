from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from users.tests import TestUtils

class TagFormTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
class TagTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
