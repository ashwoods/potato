from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.encoding import python_2_unicode_compatible
from djangae.fields import RelatedSetField, ShardedCounterField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@python_2_unicode_compatible
class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    counter = ShardedCounterField()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Ticket(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name="tickets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="created_tickets")
    assignees = RelatedSetField(
        settings.AUTH_USER_MODEL, related_name="tickets")

    def __str__(self):
        return self.title

    def get_full_title(self):
        return "%s: %s" % (self.project.title, self.title)


@receiver(post_save, sender=Project)
def initialize_project(sender, instance, created, *args, **kwargs):
    if created:
        instance.counter.populate()

@receiver(post_save, sender=Ticket)
def set_ticket_counter_on_create(sender, instance, created, *args, **kwargs):
    if created:
        instance.project.counter.increment()

@receiver(post_delete, sender=Ticket)
def set_ticket_counter_on_delete(sender, instance, *args, **kwargs):
    instance.project.counter.decrement()
