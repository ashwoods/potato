from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.views.decorators.http import require_POST
from django.utils.functional import cached_property
from django.contrib import messages
from .forms import ProjectForm, TicketForm
from .models import Project, Ticket


class ProjectContextMixin(object):

    @cached_property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super(ProjectContextMixin, self).get_context_data(**kwargs)
        context['current_project'] = self.project
        return context


class MyTicketsView(TemplateView):
    template_name = "site/my_tickets.html"

    def get_context_data(self):
        if self.request.user.is_authenticated():
            tickets = (
                Ticket.objects
                .filter(assignees=self.request.user.pk)
                .order_by('-modified')
            )
        else:
            tickets = []

        return {
            'tickets': tickets
        }


my_tickets_view = MyTicketsView.as_view()


class ProjectListView(ListView):
    model = Project
    template_name = "site/project_list.html"


project_list_view = ProjectListView.as_view()


class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "site/project_form.html"

    def get_success_url(self):
        return reverse("project-list")

    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create project'
        return kwargs


create_project_view = login_required(CreateProjectView.as_view())


class UpdateProjectView(ProjectContextMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'project_id'
    template_name = "site/project_form.html"

    def get_success_url(self):
        return reverse("project-list")

    def get_form_kwargs(self):
        kwargs = super(UpdateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)
        return kwargs


update_project_view = login_required(UpdateProjectView.as_view())


class ProjectView(ProjectContextMixin, TemplateView):
    template_name = "site/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        project = self.project
        context.update({
            "project": project,
            "tickets": project.tickets.all()
        })
        return context


project_view = ProjectView.as_view()


class CreateTicketView(ProjectContextMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "site/ticket_form.html"

    def get_success_url(self):
        return reverse("project-detail", kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(CreateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create ticket'
        return kwargs


create_ticket_view = login_required(CreateTicketView.as_view())


class UpdateTicketView(ProjectContextMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    pk_url_kwarg = 'ticket_id'
    template_name = "site/ticket_form.html"

    def get_queryset(self):
        return super(UpdateTicketView, self).get_queryset().filter(project=self.kwargs['project_id'])

    def get_success_url(self):
        return reverse("project-detail", kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(UpdateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)
        return kwargs


update_ticket_view = login_required(UpdateTicketView.as_view())


@login_required
@require_POST
def update_state_ticket_view(request, project_id, ticket_id):
    ticket = get_object_or_404(Ticket, project=project_id, pk=ticket_id)
    action = request.POST.get('transition')
    if action in [transition.name for transition in ticket.get_available_state_transitions()]:
        getattr(ticket, action)()
        ticket.save()
        #messages.success(request, 'Your ticket has been successfully %s' % action)

    return redirect(reverse('my-tickets'))
