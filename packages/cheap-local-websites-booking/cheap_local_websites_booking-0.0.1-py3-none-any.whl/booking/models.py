from django.db import models
from services.models import Service

class Client(models.Model):
    INACTIVE = 'Inactive'
    LEAD = 'Lead'
    CLIENT = 'Client'
    WEBSITE_MANAGEMENT = 'Website Management'
    STATUS = [
        (INACTIVE, 'Inactive'),
        (LEAD, 'Lead'),
        (CLIENT, 'Client'),
        (WEBSITE_MANAGEMENT, 'Website Management'),
    ]
    status = models.CharField(max_length=25, choices=STATUS, default=LEAD,)
    name = models.CharField(max_length=35)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    business_name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service)
    comments = models.TextField(max_length=1500)


    def __unicode__(self):
        return '%s' % self.name

    def __str__(self):
        return self.name