from django.db import models


class TicketTemplate(models.Model):
    template = models.TextField()

    def __str__(self):
        return 'Ticket Template'
