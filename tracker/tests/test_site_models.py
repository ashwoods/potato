from nose.tools import ok_, eq_, raises

from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory



from tracker.site.models import Project, Ticket


class ProjectModelCounterlTest(TestCase):

    def setUp(self):
        self.test_project = Project.objects.create(title='Test project')
        self.another_project = Project.objects.create(title='Another project')

    def test_ticket_counter_on_create(self):
        for i in range(1,10):
            Ticket.objects.create(project=self.test_project, title="Title %s" % i)
            eq_(self.test_project.counter.value(), i)

        Ticket.objects.create(project=self.another_project, title='Another project ticket')
        retrieve_counter = Project.objects.get(pk=self.test_project.pk).counter.value()
        eq_(retrieve_counter, 9)
        eq_(self.another_project.counter.value(), 1)

    def test_ticket_counter_on_delete(self):
        for i in range(1,10):
            Ticket.objects.create(project=self.test_project, title="Title %s" % i)
        eq_(self.test_project.counter.value(), 9)
        self.test_project.tickets.all()[0].delete()
        eq_(self.test_project.counter.value(), 8)
        self.test_project.tickets.all().delete()
        eq_(self.test_project.counter.value(), 0)

    def test_counter_on_transition(self):
        for i in range(1,10):
            Ticket.objects.create(project=self.test_project, title="Title %s" % i)
        eq_(self.test_project.counter.value(), 9)
        eq_(self.test_project.new_counter.value(), 9)
        test_ticket = self.test_project.tickets.all()[0]

        test_ticket.open()
        test_ticket.save()
        eq_(self.test_project.counter.value(), 9)
        eq_(self.test_project.new_counter.value(), 8)
        eq_(self.test_project.open_counter.value(), 1)
        test_ticket.close()
        test_ticket.save()
        eq_(self.test_project.counter.value(), 9)
        eq_(self.test_project.open_counter.value(), 0)
        eq_(self.test_project.closed_counter.value(), 1)
        test_ticket.safe_delete()
        test_ticket.save()
        eq_(self.test_project.counter.value(), 8)
        eq_(self.test_project.closed_counter.value(), 0)
        eq_(self.test_project.deleted_counter.value(), 1)


