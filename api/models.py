from django.db import models
from django.contrib.auth.models import User

class VacationRequest(models.Model):
    user = models.ForeignKey(User)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='WAITING_FOR_REVIEW')
