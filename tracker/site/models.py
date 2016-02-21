from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible
from djangae.fields import RelatedSetField, ShardedCounterField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_fsm import FSMIntegerField, transition
from django_fsm.signals import post_transition
from enum import IntEnum


@python_2_unicode_compatible
class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    counter = ShardedCounterField()
    new_counter = ShardedCounterField()
    open_counter = ShardedCounterField()
    closed_counter = ShardedCounterField()
    deleted_counter = ShardedCounterField()

    def __str__(self):
        return self.title


class TICKET_STATES(IntEnum):
    DELETED = 0
    NEW = 1
    OPEN = 2
    CLOSED = 3


@python_2_unicode_compatible
class Ticket(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    state = FSMIntegerField(default=TICKET_STATES.NEW, db_index=True)
    state_on_delete = models.IntegerField(null=True)
    project = models.ForeignKey(Project, related_name="tickets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="created_tickets")
    assignees = RelatedSetField(
        settings.AUTH_USER_MODEL, related_name="tickets")

    def __str__(self):
        return self.title

    def get_full_title(self):
        return "%s: %s" % (self.project.title, self.title)

    def get_literal_state(self):
        return TICKET_STATES(self.state)

    def get_transition_verbs(self):
        return {t.name: t.custom['verb'] for t in self.get_available_state_transitions()}

    @transition(field=state, source=TICKET_STATES.NEW, target=TICKET_STATES.OPEN, custom={'label': 'Open', 'verb': 'opened'})
    def open(self):
        pass

    @transition(field=state, source=[TICKET_STATES.NEW, TICKET_STATES.OPEN], target=TICKET_STATES.CLOSED, custom={'label': 'Close', 'verb':'closed'})
    def close(self):
        pass

    @transition(field=state, source='+', target=TICKET_STATES.DELETED, custom={'label': 'Delete', 'verb': 'deleted'})
    def safe_delete(self):
        pass


@receiver(post_save, sender=Project)
def initialize_project(sender, instance, created, *args, **kwargs):
    if created:
        instance.counter.populate()


@receiver(post_save, sender=Ticket)
def set_ticket_counter_on_create(sender, instance, created, *args, **kwargs):
    if created:
        instance.project.counter.increment()
        instance.project.new_counter.increment()


@receiver(post_delete, sender=Ticket)
def set_ticket_counter_on_delete(sender, instance, *args, **kwargs):
    if instance.state is not TICKET_STATES.DELETED:
        instance.project.counter.decrement()


@receiver(post_transition, sender=Ticket)
def set_ticket_counter_on_transition(sender, instance, name, source, target, *args, **kwargs):
    if target is TICKET_STATES.DELETED:
        instance.project.counter.decrement()
    source_counter = getattr(instance.project, '%s_counter' % TICKET_STATES(source).name.lower())
    source_counter.decrement()
    target_counter = getattr(instance.project, '%s_counter' % TICKET_STATES(target).name.lower())
    target_counter.increment()
