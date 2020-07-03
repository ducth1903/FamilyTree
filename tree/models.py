# Ref: https://docs.djangoproject.com/en/3.0/ref/models/fields/

from django.db import models

# Create your models here.
class Couple(models.Model):
    wife_name               = models.CharField(max_length=100, null=True, blank=True)
    wife_dob                = models.DateField([r'%m/%d/%Y'], null=True, blank=True)
    wife_bornPlace          = models.CharField(max_length=500, null=True, blank=True)
    wife_occupation         = models.TextField(null=True, blank=True)
    wife_email              = models.EmailField(null=True, blank=True)
    wife_deceasedDate       = models.DateField(null=True, blank=True)
    
    husband_name            = models.CharField(max_length=100, null=True, blank=True)
    husband_dob             = models.DateField([r'%m/%d/%Y'], null=True, blank=True)
    husband_bornPlace       = models.CharField(max_length=500, null=True, blank=True)
    husband_occupation      = models.TextField(null=True, blank=True)
    husband_email           = models.EmailField(null=True, blank=True)
    husband_deceasedDate    = models.DateField(null=True, blank=True)

    parent_id               = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.wife_name} - {self.husband_name}"