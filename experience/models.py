from django.db import models
from account.models import User

class ExperienceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    company_name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Company Name")
    job_title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Job Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + " : " + self.company_name