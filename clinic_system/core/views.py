from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.add_message(request, messages.INFO, 'Usuário não cadastrado no sistema')
        else:
            login(request, user)
            if request.user.person.is_medical:
                return redirect('medical-page')
            else:
                return redirect('clinic-manager-page')

    return render(request, 'core/login.html')


def person_register(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            birthday = request.POST.get('birthday')
            cpf = request.POST.get('cpf')
            password = request.POST.get('password')
            sex = request.POST.get('sex')
            contact = request.POST.get('contact')
            email = request.POST.get('email')
            salary = request.POST.get('salary')
            commission = request.POST.get('commission')
            is_medical = request.POST.get('is_medical')
            if is_medical == 'on':
                is_medical = True
            else:
                is_medical = False

            user_verify_email = User.objects.filter(email=email)

            if len(user_verify_email) == 0:
                user_verify_username = User.objects.filter(username=cpf)
                if len(user_verify_username) == 0:
                    user = User.objects.create_user(
                        username=cpf,
                        email=email,
                        password=password
                    )
                    person = Person(
                        name=name,
                        birthday=birthday,
                        cpf=cpf,
                        sex=sex,
                        contact=contact,
                        salary=salary,
                        commission=commission,
                        is_medical=is_medical,
                        user=user
                    )
                    person.save()
                    return redirect('login-page')
                else:
                    messages.add_message(request, messages.INFO, 'O CPF informado já esta cadastrado')
            else:
                messages.add_message(request, messages.INFO, 'O e-mail informado já esta cadastrado')
        except:
            messages.add_message(request, messages.INFO,
                                 'Ocorreu um erro interno, por favor entre em contato com o administrador do sistema')

    return render(request, 'core/register-person.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def medical_page(request):
    is_medical = request.user.person.is_medical
    horarios = MedicalSchedule.objects.filter(medico=request.user.id)
    agendamentos_confirmados = MedicalAppointment.objects.filter(status='Agendamento confirmado')
    if not is_medical:
        messages.add_message(request, messages.INFO,
                             'Você não possui permissão para acessar a página de gerenciamento de consultas, você foi '
                             'redirecionado')
        return redirect('clinic-manager-page')
    return render(request, 'core/medical-management.html', {'horarios':horarios, 'agendamentos':agendamentos_confirmados})


@login_required(login_url='login')
def clinic_manager_page(request):
    is_medical = request.user.person.is_medical
    agendamentos = MedicalAppointment.objects.filter(status='Agendado')

    if is_medical:
        messages.add_message(request, messages.INFO,
                             'Você não possui permissão para acessar a página de gerenciamento médico, você foi '
                             'redirecionado')
        return redirect('medical-page')
    
    patients = Patient.objects.all()
    return render(request, 'core/clinic-management.html', { 'patients': patients, 'agendamentos':agendamentos})


@login_required(login_url='login')
def patient_page(request):
    is_medical = request.user.person.is_medical
    if is_medical:
        messages.add_message(request, messages.INFO,
                             'Você não possui permissão para acessar a página de gerenciamento médico, você foi '
                             'redirecionado')
        return redirect('medical-page')

    if request.method == 'POST':
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        cpf = request.POST.get('cpf')
        sex = request.POST.get('sex')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        patient_cpf = Patient.objects.filter(cpf=cpf)
        if len(patient_cpf) == 0:
            patient = Patient(name=name, birthday=birthday, cpf=cpf, sex=sex, contact=contact, email=email)
            patient.save()
            messages.add_message(request, messages.INFO, '{} cadastrado com sucesso'.format(name))
        else:
            messages.add_message(request, messages.INFO, 'CPF informado já cadastrado')
    
    return render(request, 'core/register-patient.html')


@login_required(login_url='login')
def cadastrar_planos(request):
    if str(request.method == 'POST'):
        form = PlanosForms(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Plano cadastrado com sucesso!')
            form.save()
    else:
        form = PlanosForms()
    
    plans = MecialPlan.objects.all()

    return render(request, 'core/cadastrar-planos.html', {'form':form, 'plans': plans})

@login_required(login_url='login')
def cadastrar_consulta(request):
    pacientes = Patient.objects.all()
    disponibilidade = MedicalSchedule.objects.all()
    if str(request.method == 'POST'):
        form = AgendamentoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
    else:
        form = AgendamentoForm()

    return render(request, 'core/cadastro-consultas.html', {'form':form, 'pacientes':pacientes, 'disponibilidade':disponibilidade})

@login_required(login_url='login')
def cadastrar_horario(request):
    if str(request.method == 'POST'):
        form = AgendaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário cadastrado com sucesso!')
            redirect('medical-page')
        print('form - inalido')
    else:
        form = AgendaForm()

    hours = MedicalSchedule.objects.filter(medico=request.user.person)
    return render(request, 'core/cadastro-horario.html', {'form': form, 'hours': hours})

@login_required(login_url='login')
def confirmar_agendamento(request, pk):

    if str(request.method == 'POST'):
        agendamento = MedicalAppointment.objects.filter(id=pk).update(status='Agendamento confirmado')
        return redirect('clinic-manager-page')

@login_required(login_url='login')
def criar_consulta(request, pk):
    if str(request.method == 'POST'):
        form = ConsultaForm(request.POST or None)
        if form.is_valid():
            messages.add_message(request, 'Consulta finalizada')
           # form.save()
    else:
        form = ConsultaForm()

    return render(request, 'core/criar-consulta-medico.html', {'form':form})
