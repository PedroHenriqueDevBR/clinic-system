from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255, null=False)
    birthday = models.DateField()
    cpf = models.CharField(max_length=15)
    sex = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    salary = models.FloatField()
    commission = models.FloatField()
    is_medical = models.BooleanField(default=False)

    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE)
    
    @property
    def email(self):
        return self.usuario.email

'''Plano'''
class MecialPlan(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)

'''Paciente'''
class Patient(models.Model):
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    cpf = models.CharField(max_length=15)
    sex = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=255)

'''Agenda médica'''
class MedicalSchedule(models.Model):
    date = models.DateField()
    init_hour = models.TimeField()
    end_hour = models.TimeField()
    medico = models.ForeignKey(Person, on_delete=models.CASCADE)


'''Agendamento'''
class MedicalAppointment(models.Model):
    register_date = models.DateField(auto_now_add=True)
    #consultation_date = models.DateField(auto_now=False, auto_now_add=False)
    is_authorized = models.BooleanField(default=False)
    paciente = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disponibilidade_medic = models.ForeignKey(MedicalSchedule, on_delete=models.CASCADE)
    recepcionista = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=255, default='Agendado')


'''Consulta'''
class Consultation(models.Model):
    register_date = models.DateField(auto_now_add=True)
    observations = models.TextField(max_length=500)
    paciente = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disponibilidade_medic = models.ForeignKey(MedicalSchedule, on_delete=models.CASCADE)
    recepcionista = models.ForeignKey(Person, on_delete=models.CASCADE)

