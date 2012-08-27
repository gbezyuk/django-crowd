from django.test import TestCase
from django.test.utils import override_settings
from .backends import CrowdBackend
from django.contrib.auth.models import User

class CrowdBackendAuthTest(TestCase):
    """
    Basic test suite for django_crowd (Attlasian CROWD (JIRA) Authentication Backend for Django) CrowdBackend
    """
    def setUp(self):
        """
        Initialization
        """
        self.backend = CrowdBackend()
        self.username = 'gbezyuk'
        self.password = 'password'
        self.email = 'gbezyuk@gmail.com'
        self.first_name = 'Grigoriy'
        self.last_name = 'Beziuk'
        self.test_crowd_xml_response = """
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <user name="%(username)s" expand="attributes">
            <link rel="self" href="http://samplecrowd/crowd/rest/usermanagement/latest/user?username=%(username)s"/>
            <first-name>%(first_name)s</first-name>
            <last-name>%(last_name)s</last-name>
            <display-name>%(first_name)s %(last_name)s</display-name>
            <email>%(email)s</email>
            <password>
                <link rel="edit" href="http://samplecrowd/crowd/rest/usermanagement/latest/user/password?username=%(username)s"/>
            </password>
            <active>true</active>
            <attributes>
                <link rel="self" href="http://samplecrowd/crowd/rest/usermanagement/latest/user/attribute?username=%(username)s"/>
            </attributes>
        </user>
        """.strip() % {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    @override_settings(CROWD=None)
    def test_crowd_configuration_is_required(self):
        """
        If no CROWD settings provided, UserWarning should be raised - testing that
        """
        self.assertRaises(UserWarning, self.backend.authenticate, self.username, self.password)

    def test_parse_crowd_response(self):
        """
        CROWD API returns an XML with user information. Mocking this result, testing that we can parse it properely
        """
        parse_result = self.backend._parse_crowd_response(self.test_crowd_xml_response)
        self.assertEqual(parse_result['email'], self.email)
        self.assertEqual(parse_result['first_name'], self.first_name)
        self.assertEqual(parse_result['last_name'], self.last_name)

    def test_creating_new_user_from_provided_crowd_response(self):
        """
        Test creating new user from CROWD response
        """
        users_existed = User.objects.all().count() # usually == 0, but who knows, which fixture they will use... =)
        user_created = self.backend._create_new_user_from_crowd_response(username=self.username,
            password=self.password, content=self.test_crowd_xml_response, crowd_config={})
        self.assertEqual(users_existed + 1, User.objects.all().count())
        self.assertEqual(user_created.username, self.username)
        self.assertEqual(user_created.email, self.email)
        self.assertEqual(user_created.first_name, self.first_name)
        self.assertEqual(user_created.last_name, self.last_name)

    def find_existing_user(self):
        """
        A little unit test for a service method
        """
        self.assertEqual(self.backend._find_existing_user(self.username), None)
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.assertNotEqual(self.backend._find_existing_user('not_a_' + self.username   ), None)
        self.assertEqual(self.backend._find_existing_user(self.username).pk, user.pk)
