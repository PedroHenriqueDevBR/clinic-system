
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_page, name='login'),
    path('login/', login_page, name='login-page'),
    path('logout/', logout_page, name='logout-page'),
    path('cadastrar/', person_register, name='register-person-page'),
    path('dashboard/', clinic_manager_page, name='clinic-manager-page'),
    path('dashboard/paciente/', patient_page, name='patient-page'),
    path('gerenciamento/', medical_page, name='medical-page'),
    path('cadastro/planos', cadastrar_planos, name='cadastrar-planos'),
    path('cadastro/consultas', cadastrar_consulta, name='cadastro-consultas'),
    path('cadastro/horarios', cadastrar_horario, name='cadastrar-horario'),
    path('confirmar/agendamento/<int:pk>', confirmar_agendamento, name='confirmar-agendamento'),
    path('criar/consulta/<int:pk>', criar_consulta, name='criar-consulta'),
]