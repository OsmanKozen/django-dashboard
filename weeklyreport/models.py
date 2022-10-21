from django.db import models
import datetime


class Reports(models.Model):
    weeknum = datetime.date.today().isocalendar()[1]
    type = models.CharField(max_length=50,  default='Highlight')
    priority = models.IntegerField(default=4)
    service = models.CharField(
        max_length=300, default='', blank=True, null=True)
    entry_owner = models.CharField(max_length=300, )
    entry = models.TextField(default='')
    entry_date = models.DateTimeField(auto_now_add=True, blank=True)
    team = models.CharField(max_length=100, default='')
    unit = models.CharField(max_length=100, default='')
    manager = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.entry_owner + '--- ' + self.entry

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
        return self.managername