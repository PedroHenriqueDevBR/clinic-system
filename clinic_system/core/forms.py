from django import forms
from .models import *

class PlanosForms(forms.ModelForm):
    class Meta:
        model = MecialPlan
        fields = '__all__'

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = MedicalAppointment
        fields = '__all__'

    def clean(self):
        x = self.cleaned_data
        print(x)

class AgendaForm(forms.ModelForm):
    class Meta:
        model = MedicalSchedule
        fields = '__all__'

    def clean(self):
        x = self.cleaned_data
        print(x)

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = '__all__'