from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django_dynamic_fixture import N, G
from issue_models.models import MyUser, Project, Story
from django.core.urlresolvers import reverse


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


class UpdateProfileTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/profile/update/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_profile_update(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/profile/update/')
        self.assertEqual(response.status_code, 200)

    def test_update(self):

        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/profile/update/', {'first_name': 'A', 'last_name': 'b',
                                                              'dob': '1992-02-02', })
        self.assertRedirects(response, '/home/profile/')


class CreateProjectTest(TestCase):
    def setUp(self):
        self.member = G(MyUser)
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/create/project/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_profile_update(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/create/project/')
        self.assertEqual(response.status_code, 200)

    def test_valid_project_create(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/create/project/', {'project_title': 'demo project',
                                                              'description': 'trying project',
                                                              'assigned_to': self.member.id})
        self.assertRedirects(response, '/home/dashboard/')

    def test_invalid_project_create(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/create/project/', {'project_title': '',
                                                              'description': 'trying project',
                                                              'assigned_to': self.member.id})
        self.assertEqual(response.status_code, 200)


class ProjectTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/project/3/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_project(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('project', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_non_member(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('project', kwargs={'pk': '50'}))
        self.assertEqual(response.status_code, 404)


class ProjectUpdateTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/projects/update/13/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_update_project_access(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('updateproject', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_non_member(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('updateproject', kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, 404)

    def test_authenticate_update_project(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updateproject', kwargs={'pk': self.project.id}),
                                    {'project_title': 'abcd',
                                     'description': 'abcd1',
                                     'assigned_to': [self.member.id, self.instance.id]})
        self.assertRedirects(response, (reverse('project', kwargs={'pk': self.project.id})))

    def test_authenticate_update_project_missing_data(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updateproject', kwargs={'pk': self.project.id}),
                                    {'project_title': 'abcd',
                                     'assigned_to': [self.member.id, self.instance.id]})
        self.assertEqual(response.status_code, 200)


class AddStoryTest(TestCase):
    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project)
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/projects/story/add/8/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_Add_Story_access(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('addstory', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_non_member(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('addstory', kwargs={'pk': '15'}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_add_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('addstory', kwargs={'pk': self.project.id}),
                                    {'story_title': 'story1',
                                     'description': 'About Story',
                                     'assignee': self.member.id,
                                     'estimate': 1,
                                     'scheduled': 'no'})
        self.assertRedirects(response, (reverse('project', kwargs={'pk': self.project.id})))

    def test_authenticated_user_add_story_missing_value(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('addstory', kwargs={'pk': self.project.id}),
                                    {'description': 'About Story',
                                     'assignee': self.member.id,
                                     'estimate': 1,
                                     'scheduled': 'no'})
        self.assertEqual(response.status_code, 200)


class UpdateStoryTest(TestCase):
    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project)
        self.story = G(Story, project_title=self.project, email=self.instance)
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/projects/story/update/32/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_Add_Story_access(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('updatestory', kwargs={'pk': self.story.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_non_member(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('updatestory', kwargs={'pk': '15'}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_update_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updatestory', kwargs={'pk': self.story.id}),
                                    {'story_title': 'story1',
                                     'description': 'About Story',
                                     'assignee': self.member.id,
                                     'estimate': 1,
                                     'scheduled': 'no',
                                     'status': 'unstrtd'})
        self.assertRedirects(response, (reverse('project', kwargs={'pk': self.project.id})))

    def test_authenticated_user_update_story_missing_value(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updatestory', kwargs={'pk': self.story.id}),
                                    {'description': 'About Story',
                                     'assignee': self.member.id,
                                     'estimate': 1,
                                     'scheduled': 'no'})
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_update_story_wrong_status(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updatestory', kwargs={'pk': self.story.id}),
                                    {'story_title': 'story1',
                                     'description': 'About Story',
                                     'assignee': self.member.id,
                                     'estimate': 1,
                                     'scheduled': 'no',
                                     'status': 'finish'})
        self.assertEqual(response.status_code, 200)