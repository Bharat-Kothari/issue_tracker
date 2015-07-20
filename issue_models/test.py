from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django_dynamic_fixture import N
from issue_models.models import MyUser


class SignupTest(TestCase):
    def test_signup_valid(self):
        response = self.client.post('/home/signup/', {'email': 'abc@abc.com',
                                                      'password': 'IndiaA1!',
                                                      'confirm_password': 'IndiaA1!',
                                                      'first_name': 'A',
                                                      'last_name': 'b',
                                                      'dob': '1992-02-02', })
        self.assertRedirects(response, '/home/dashboard/')

    def test_signup_invalid(self):
        response = self.client.post('/home/signup/', {'email': 'abc@abc.com',
                                                      'password': 'IndiaA1!',
                                                      'confirm_password': 'IndiaA1',
                                                      'first_name': 'A',
                                                      'last_name': 'b',
                                                      'dob': '1992-02-02', })
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):
    def setUp(self):
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_login_correctly(self):
            response = self.client.post('/home/login/', {'email': self.instance.email, 'password': self.password})
            # print response
            self.assertRedirects(response, '/home/dashboard/')

    def test_login_incorrectly(self):
        response = self.client.post('/home/login/', {'email': self.instance.email, 'password': 'abc'})
        self.assertEqual(response.status_code, 200)


class DashboardTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/dashboard/')
        self.assertRedirects(response, 'home/login/')

    def test_authenticated_user(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/dashboard/')
        self.assertEqual(response.status_code, 200)


class ProfileTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/profile/')
        self.assertRedirects(response, 'home/login/')

    def test_authenticated_user_profile(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/profile/')
        self.assertEqual(response.status_code, 200)