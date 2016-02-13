from nose.tools import ok_, eq_

from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory


from django_nose.tools import assert_code, assert_ok

from tracker.site import views
from tracker.site.models import Project, Ticket


class ProjectViewTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = get_user_model().objects.pre_create_google_user(email='ashwoods@gmail.com')
        self.test_project = Project.objects.create(title='Another Test project')
        self.project_kwargs = {'project_id': self.test_project.pk}

    def test_project_list_view(self):
        request = self.rf.get(reverse('project-list'))
        response = views.project_list_view(request)
        assert_code(response, 200)

    def test_anonymous_create_project_view(self):
        request = self.rf.get(reverse('project-create'))
        request.user = AnonymousUser()
        response = views.create_project_view(request)
        assert_code(response, 302)

    def test_user_create_project_view_get(self):
        request = self.rf.get(reverse('project-create'))
        request.user = self.user
        response = views.create_project_view(request)
        assert_code(response, 200)
        ok_(response.render())  # added to catch crispy bug issue:#1

    def test_user_create_project_view_post_error(self):
        request = self.rf.post(reverse('project-create'))
        request.user = self.user
        response = views.create_project_view(request)
        ok_(not response.context_data['form'].is_valid())

    def test_user_create_project_view_post_success(self):
        request = self.rf.post(reverse('project-create'), {'title': 'Test project'})
        request.user = self.user
        response = views.create_project_view(request)
        assert_code(response, 302)
        eq_(response['location'], '/projects/')
        ok_(Project.objects.get(title='Test project'))

    def test_user_update_project_view_get(self):
        request = self.rf.get(reverse('project-update', kwargs=self.project_kwargs))
        request.user = self.user
        response = views.update_project_view(request, **self.project_kwargs)
        assert_code(response, 200)
        ok_(response.render())

    def test_user_update_project_view_post_error(self):
        request = self.rf.post(reverse('project-update', kwargs=self.project_kwargs))
        request.user = self.user
        response = views.update_project_view(request, **self.project_kwargs)
        ok_(not response.context_data['form'].is_valid())

    def test_user_update_project_view_post_success(self):
        new_title = 'Changed Title'
        request = self.rf.post(reverse('project-update', kwargs=self.project_kwargs), {'title': new_title})
        request.user = self.user
        response = views.update_project_view(request, **self.project_kwargs)
        assert_code(response, 302)
        eq_(response['location'], reverse('project-list'))
        project = Project.objects.get(pk=self.test_project.pk)
        ok_(project.title == new_title)


class TicketViewTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.test_project = Project.objects.create(title='Test project')
        self.project_kwargs = {'project_id': self.test_project.pk}
        self.user = get_user_model().objects.pre_create_google_user(email='ashwoods@gmail.com')
        self.form_post_data = {'title': 'Test ticket',
                               'description': 'this is a short description',
                               'assignees': [self.user.pk]}
        self.test_ticket = Ticket.objects.create(title='One test ticket',
                                                 description='this is a short description',
                                                 project=self.test_project,
                                                 )
        self.test_ticket.assignees.add(self.user)
        self.ticket_kwargs = {'project_id': self.test_project.pk, 'ticket_id': self.test_ticket.pk}

    def test_user_create_ticket_get(self):
        request = self.rf.get(reverse('ticket-create', kwargs=self.project_kwargs))
        request.user = self.user
        response = views.create_ticket_view(request, **self.project_kwargs)
        assert_code(response, 200)
        ok_(response.render())

    def test_user_create_ticket_post_error(self):
        request = self.rf.post(reverse('ticket-create', kwargs=self.project_kwargs))
        request.user = self.user
        response = views.create_ticket_view(request, **self.project_kwargs)
        ok_(not response.context_data['form'].is_valid())

    def test_user_create_ticket_view_post_success(self):
        request = self.rf.post(reverse('ticket-create', kwargs=self.project_kwargs), self.form_post_data)
        request.user = self.user
        response = views.create_ticket_view(request, **self.project_kwargs)
        assert_code(response, 302)
        eq_(response['location'], reverse('project-detail', kwargs=self.project_kwargs))
        ticket = Ticket.objects.get(title='Test ticket')
        ok_(ticket)
        ok_(request.user in ticket.assignees.all())

    def test_user_update_ticket_view_get(self):
        request = self.rf.get(reverse('ticket-update', kwargs=self.ticket_kwargs))
        request.user = self.user
        response = views.update_ticket_view(request, **self.ticket_kwargs)
        assert_code(response, 200)
        ok_(response.render())

    def test_user_update_ticket_view_post_error(self):
        request = self.rf.post(reverse('ticket-update', kwargs=self.ticket_kwargs))
        request.user = self.user
        response = views.update_ticket_view(request, **self.ticket_kwargs)
        ok_(not response.context_data['form'].is_valid())

    def test_user_update_ticket_view_post_success(self):
        request = self.rf.post(reverse('ticket-update', kwargs=self.ticket_kwargs), self.form_post_data)
        request.user = self.user
        response = views.update_ticket_view(request, **self.ticket_kwargs)
        assert_code(response, 302)
        eq_(response['location'], reverse('project-detail', kwargs=self.project_kwargs))
        ticket = Ticket.objects.get(pk=self.test_ticket.pk)
        ok_(ticket.title == self.form_post_data.get('title'))
        ok_(request.user in ticket.assignees.all())

    def test_user_project_view(self):
        request = self.rf.get(reverse('project-detail', kwargs=self.project_kwargs))
        request.user = self.user
        response = views.project_view(request, **self.project_kwargs)
        assert_code(response, 200)

    def test_user_my_tickets_view(self):
        request = self.rf.get(reverse('my-tickets'))
        request.user = self.user
        response = views.my_tickets_view(request)
        assert_code(response, 200)
