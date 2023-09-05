from django.db import models
import datetime
from django.core.validators import FileExtensionValidator, ValidationError

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Maximum Image boyutu %sMB" % str(megabyte_limit))
    
class Reports(models.Model):
    weeknum = datetime.date.today().isocalendar()[1]
    yearnum = datetime.date.today().year
    
    type = models.CharField(max_length=50,  default="Highlight")
    priority = models.IntegerField(default=4)
    service = models.CharField(max_length=300, default="", blank=True, null=True)
    entry_owner = models.CharField(max_length=300)
    entry = models.TextField(default="")
    document = models.FileField(upload_to="""REPORT/documents/uploads/{0}/{1}""".format(yearnum, weeknum), validators=[validate_image, FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])], blank=True)
    entry_date = models.DateTimeField(auto_now_add=True, blank=True)
    team = models.CharField(max_length=100, default="")
    unit = models.CharField(max_length=100, default="")
    manager = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.entry_owner

class Services(models.Model):
    servicename = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, default='')
    teamname = models.CharField(max_length=100, default='')
    unitname = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.servicename

class Users(models.Model):
    username = models.CharField(max_length=100, default='')
    teamname = models.CharField(max_length=100, default='')
    unitname = models.CharField(max_length=100, default='')
    mail = models.CharField(max_length=200, default='')
    phone = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.username

class Teams(models.Model):
    teamname = models.CharField(max_length=100, default='')
    unitname = models.CharField(max_length=100, default='')
    manager_mail = models.CharField(max_length=500, default='')
    unithead_mail = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.teamname

class Units(models.Model):
    unitname = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.unitname

class Managers(models.Model):
    managername = models.CharField(max_length=100, default='')
    teamname = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.teamname