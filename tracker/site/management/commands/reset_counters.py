from django.core.management.base import BaseCommand, CommandError
from tracker.site.models import Project

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        counter = 0
        STATES = {'deleted': 0, 'new': 1, 'open': 2, 'closed': 3}
        for project in Project.objects.all():
            project_counter = 0
            project.counter.reset()
            for key, value in STATES.iteritems():
                getattr(project, '%s_counter' % key).reset()
                state_counter = project.tickets.filter(state=value).count()
                getattr(project, '%s_counter' % key).increment(state_counter)
                counter += state_counter
                project_counter += state_counter
            project.counter.increment(project_counter)

        self.stdout.write('Reset %s tickets' % counter)
