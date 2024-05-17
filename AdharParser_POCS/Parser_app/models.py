from django.db import models

# Create your models here.

class AdharFile(models.Model):
    file = models.FileField(blank=True, null=True)
    name = models.CharField(blank=True,null=True,max_length=50)
    dob = models.CharField(blank=True,null=True, max_length=50)
    adhar_number = models.CharField(blank=True,null=True, max_length=50)
    gender = models.CharField(blank=True,null=True, max_length=50)
    address = models.TextField(blank=True,null=True, max_length=50)
    
    
    
class PanParser(models.Model):
    pan_number = models.CharField(
        max_length = 30,
        verbose_name = 'Pan_Number'
    )
    date_of_birth = models.DateField(
        verbose_name = 'DOB'
    )
    name = models.CharField(
        max_length=50,
        verbose_name = 'Name'
    )
    father_name = models.CharField(
        max_length = 50,
        verbose_name = 'Father_Name'
    )

    def __str__(self) -> str:
        return self.name + ' - ' + self.pan_number

