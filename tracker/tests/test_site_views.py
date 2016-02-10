
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from django_nose.tools import assert_code

from tracker.site.views import project_list_view, create_project_view


rf = RequestFactory()
user = get_user_model().objects.pre_create_google_user(email='ashwoods@gmail.com')


def test_project_list_view():
    request = rf.get(reverse('project-list'))
    response = project_list_view(request)
    assert_code(response, 200)



