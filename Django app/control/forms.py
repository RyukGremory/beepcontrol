from django.forms import ModelForm
from .models import Control

class ControlForm(ModelForm):
    class Meta:
        model = Control
        fields = ['room','user','accion']