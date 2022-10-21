from django import forms
from .models import *

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = "__all__"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = "__all__"