
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from django_nose.tools import assert_code, assert_ok

from tracker.site.views import project_list_view, create_project_view


class SiteViewTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = get_user_model().objects.pre_create_google_user(email='ashwoods@gmail.com')

    def test_project_list_view(self):
        request = self.rf.get(reverse('project-list'))
        response = project_list_view(request)
        assert_code(response, 200)

    def test_anonymous_create_project_view(self):
        request = self.rf.get(reverse('project-create'))
        request.user = AnonymousUser()
        response = create_project_view(request)
        assert_code(response, 302)

    def test_user_create_project_view_get(self):
        request = self.rf.get(reverse('project-create'))
        request.user = self.user
        response = create_project_view(request)
        assert_code(response, 200)
        assert(response.render())

