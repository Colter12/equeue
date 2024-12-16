from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from userapp.models import Ticket, Operator
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('operator_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'operatorapp/login.html', {'form': form})


@login_required
def operator_dashboard(request):
    operator = get_object_or_404(Operator, user=request.user)
    waiting_tickets = Ticket.objects.filter(status='waiting').order_by('issued_at')
    in_service_tickets = Ticket.objects.filter(status='in_service', operator=operator).order_by('issued_at')
    served_tickets = Ticket.objects.filter(status='served', operator=operator).order_by('-issued_at')[:5]
    operators = Operator.objects.exclude(user=request.user)

    return render(request, 'operatorapp/dashboard.html', {
        'operator': operator,
        'waiting_tickets': waiting_tickets,
        'in_service_tickets': in_service_tickets,
        'served_tickets': served_tickets,
        'operators': operators,
    })


@login_required
def call_ticket(request, ticket_id):
    operator = get_object_or_404(Operator, user=request.user)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'in_service'
    ticket.operator = operator
    ticket.save()
    return redirect('operator_dashboard')


@login_required
def start_service(request, ticket_id):
    if request.method == 'POST':
        operator = get_object_or_404(Operator, user=request.user)
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.status = 'in_service'
        ticket.start_time = timezone.now()
        ticket.operator = operator
        ticket.save()
        return JsonResponse({'success': True})
    return HttpResponseNotAllowed(['POST'])


@login_required
def finish_service(request, ticket_id):
    operator = get_object_or_404(Operator, user=request.user)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'served'
    ticket.is_served = True
    ticket.end_time = timezone.now()
    ticket.served_by = request.user.username

    if ticket.start_time and ticket.end_time:
        duration = ticket.end_time - ticket.start_time
        seconds = int(duration.total_seconds())
        formatted_duration = str(timedelta(seconds=seconds))
        ticket.duration = formatted_duration
        ticket.save()

    return redirect('operator_dashboard')


@login_required
def cancel_service(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'served'
    ticket.is_canceled = True
    ticket.save()
    return redirect('operator_dashboard')


@login_required
def redirect_ticket(request, ticket_id):
    if request.method == 'POST':
        operator_id = request.POST.get('operator_id')
        print("Received operator_id:", operator_id, "for ticket_id:", ticket_id)  # Debugging output

        new_operator = get_object_or_404(Operator, id=operator_id)
        ticket = get_object_or_404(Ticket, id=ticket_id)

        ticket.operator = new_operator
        ticket.status = 'waiting'
        ticket.save()

        print("Ticket", ticket_id, "redirected to operator", operator_id)  # Confirmation output
        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['POST'])


