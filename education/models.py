from django.db import models
from account.models import User

class EducationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    institution_name = models.CharField(max_length=255, verbose_name="Institution Name", null=False, blank=False)
    major = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cgpa = models.FloatField(null=True, blank=True, verbose_name="CGPA")


    def __str__(self):
        return self.user.get_full_name()+" : "+self.institution_name
