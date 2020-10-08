from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    # Creating setup function: function that is ran before every test that we run, so sometimes there are setup tasks
    # that need to be done before every test in our test case class. So we can do this using a setup function

    def setUp(self):
        #  our setup is going consist of creating our test client , a new user that we can use to test we're going
        #  , make sure the user is logged into our client and finally we're going to create a regular user that is not
        # authenticated or that we can use to list in our admin page.

        self.Client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email='admin@londonappdev.com',
                                                                    password='password123')
        self.client.force_login(self.admin_user)
        # It uses the client helper function that allows you to log a user in with the Django authentication and this
        # really helps make our tests a lot easier to write because it means we don't have to manually log the user
        # in we can just use this helper function.
        self.user = get_user_model().objects.create_user(email="test@londonappdev.com", password='password123',
                                                         name='Test user full name')

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        #  /admin/core/user/1
        res = self.client.get(url)  # http.get to the url
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
