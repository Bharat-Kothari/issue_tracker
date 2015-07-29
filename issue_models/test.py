from _elementtree import tostring
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django_dynamic_fixture import N, G
from issue_models.models import MyUser, Project, Story
from django.core.urlresolvers import reverse
import json


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


class LogoutTest(TestCase):
    def setUp(self):
        self.instance = N(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        return self.instance

    def test_logout_authenticated_user(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/dash/logout/')
        self.assertRedirects(response,'/home/')

    def test_logout_unauthenticated_user(self):
        response = self.client.get('/home/dash/logout/')
        self.assertRedirects(response,'/home/login/')


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
        response1 = self.client.get(reverse('dashboard')+'?id=1')

        response2 = self.client.get(reverse('dashboard')+'?id=2')
        response3 = self.client.get(reverse('dashboard')+'?id=3')
        if response1.status_code==response2.status_code and response1.status_code==response3.status_code:
            self.assertEqual(response1.status_code, 200)

    def test_authenticated_user_access_login(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get('/home/login/')
        self.assertRedirects(response,'/home/dashboard/')


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

    def test_update_profile(self):

        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/profile/update/', {'first_name': 'A', 'last_name': 'b',
                                                              'dob': '1992-02-02', })
        self.assertRedirects(response, '/home/profile/')

    def test_update_password(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/profile/update/',{'old_password':self.password,
                                                             'new_password1':'aaaaaA1!',
                                                             'new_password2':'aaaaaA1!',
                                                             'form2': True   })
        self.assertRedirects(response, '/home/profile/')

    def test_update_password_miss_match(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post('/home/profile/update/',{'old_password':self.password,
                                                             'new_password1':'aaaaaA1!',
                                                             'new_password2':'aaaaaA1',
                                                             'form2': True   })

        self.assertEqual(response.status_code, 200)

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
        self.member2 = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project,project_manager=self.member, assigned_to=[self.member, self.member2])
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
        response = self.client.get(reverse('project', kwargs={'pk': self.project2.id}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_no_project(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('project', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, 404)


class ProjectUpdateTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.member1 = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project, project_manager=self.member, assigned_to=[self.member, self.member1])
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
        response = self.client.get(reverse('updateproject', kwargs={'pk': self.project2.id}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_no_project(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('updateproject', kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, 404)


    def test_authenticate_update_project(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updateproject', kwargs={'pk': self.project.id}),
                                    {'project_title': 'abcd',
                                     'description': 'abcd1',
                                     'assigned_to': [self.member1.id, self.member.id, self.instance.id]})
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
                                    {
                                     'form-0-story_title': 'story1',
                                     'form-0-description': 'About Story',
                                     'form-0-assignee': self.member.id,
                                     'form-0-estimate': 1,
                                     'form-0-scheduled': 'no',
                                      'form-TOTAL_FORMS': 1,
                                       'form-INITIAL_FORMS': 0,})
        self.assertRedirects(response, (reverse('project', kwargs={'pk': self.project.id})))
    def test_authenticated_user_add_story_missing_value(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('addstory', kwargs={'pk': self.project.id}),
                                    {'form-description': 'About Story',
                                     'form-assignee': self.member.id,
                                     'form-estimate': 1,
                                     'form-scheduled': 'no',
                                     'form-TOTAL_FORMS': 1,
                                     'form-INITIAL_FORMS': 0,})
        self.assertEqual(response.status_code, 200)


class StoryTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project, project_manager=self.member, assigned_to=[self.member])
        self.story = G(Story, project_title=self.project, email=self.instance)
        self.story2 = G(Story, project_title=self.project2,email=self.member)
        self.story3 = G(Story, project_title=self.project2, email=self.member, visibility=False)
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/projects/story/update/32/')
        self.assertRedirects(response, '/home/login/')

    def test_authenticated_user_view_story_access(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('storyview', kwargs={'pk': self.story.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_not_access_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('storyview', kwargs={'pk': self.story2.id}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_not_visible_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('storyview', kwargs={'pk': self.story3.id}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_search_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        kwargs={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = self.client.get(reverse('searchstory', kwargs={'pk':self.project.id}), {'search_text':self.story.story_title}, **kwargs)
        checks = Story.objects.filter(story_title__icontains=self.story.story_title, visibility='ys')
        final_check = [{'story_title': check.story_title} for check in checks]
        self.assertJSONEqual(response.content,json.dumps(final_check))

    def test_authenticated_user_search_story_no_key(self):
        self.client.login(email=self.instance.email, password=self.password)
        kwargs={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = self.client.get(reverse('searchstory', kwargs={'pk':self.project.id}), {'search_text':','}, **kwargs)
        checks = Story.objects.filter(story_title__icontains=self.story.story_title, visibility='ys')
        final_check = [{'story_title': "Please enter search word"}]
        self.assertJSONEqual(response.content,json.dumps(final_check))


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

    def test_authenticated_user_update_story_wrong_condition(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.post(reverse('updatestory', kwargs={'pk': self.story.id}),
                                    {'story_title': 'story1',
                                     'description': 'About Story',
                                     'assignee': None,
                                     'estimate': 1,
                                     'scheduled': 'ys',
                                     'status': 'strtd'})
        self.assertEqual(response.status_code, 200)


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


class DeleteStoryTest(TestCase):

    def setUp(self):
        self.instance = N(MyUser)
        self.member = G(MyUser)
        self.password = self.instance.password
        self.instance.password = make_password(self.password)
        self.instance.save()
        self.project = G(Project, project_manager=self.instance, assigned_to=[self.member, self.instance])
        self.project2 = G(Project)
        self.story = G(Story, project_title=self.project, email=self.instance)
        self.story2 = G(Story, project_title=self.project2, email=self.member)
        return self.instance

    def test_unauthenticated_user(self):
        response = self.client.post('/home/projects/story/delete/62/')
        self.assertRedirects(response, '/home/login/')

    def test_delete_own_project_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('storydelete',kwargs={'pk': self.story.id}))
        self.assertRedirects(response,reverse('project',kwargs={'pk': self.project.id}))

    def test_delete_others_project_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('storydelete',kwargs={'pk': self.story2.id}))
        self.assertEqual(response.status_code, 404)


class ProjectSettingsTest(TestCase):

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

    def test_authenticated_user_project_settings_access(self):
        self.client.login(email=self.instance.email, password=self.password)
        response = self.client.get(reverse('project_settings', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_search_story(self):
        self.client.login(email=self.instance.email, password=self.password)
        kwargs={'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = self.client.get(reverse('project_settings', kwargs={'pk':self.project.id}), {'initial_date':'2015-07-27','final_date':'2015-07-29'}, **kwargs)
        print response['content-type']

        self.assertEqual(response['content-type'],'html')
        print 'here'
        self.assertEqual(response.status_code,200)
