from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
import csv
from userapp.models import Ticket
from datetime import datetime, timedelta
from django.utils import timezone


def download_stats(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ticket_stats.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ticket Number', 'Issued At', 'Served By', 'Category'])

    tickets = Ticket.objects.all()

    for ticket in tickets:
        writer.writerow([
            ticket.number,
            ticket.issued_at,
            ticket.served_by,
            ticket.subcategory.category.name if ticket.subcategory and ticket.subcategory.category else ''
        ])

    return response


def stats_view(request):
    tickets = Ticket.objects.all()
    return render(request, 'adminapp/stats.html', {'tickets': tickets})


def statistics_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_tickets = Ticket.objects.count()
        processed_tickets = Ticket.objects.filter(status='served').count()
        in_progress_tickets = Ticket.objects.filter(status='in_service').count()
        return JsonResponse({
            'total_tickets': total_tickets,
            'processed_tickets': processed_tickets,
            'in_progress_tickets': in_progress_tickets,
        })

    total_tickets = Ticket.objects.count()
    processed_tickets = Ticket.objects.filter(status='served').count()
    in_progress_tickets = Ticket.objects.filter(status='in_service').count()

    context = {
        'total_tickets': total_tickets,
        'processed_tickets': processed_tickets,
        'in_progress_tickets': in_progress_tickets,
    }
    return render(request, 'adminapp/statistics.html', context)


def filter_statistics(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start_datetime = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_datetime = timezone.make_aware(
                datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))  # Включаем конец дня

            tickets = Ticket.objects.filter(issued_at__range=[start_datetime, end_datetime])

            def format_duration(duration):
                if duration:
                    total_seconds = int(duration.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    return f"{hours:02}:{minutes:02}:{seconds:02}"
                return "Не указано"

            data = [
                {
                    'operator': ticket.served_by or 'Не указан',
                    'window': ticket.operator.window_number if ticket.operator else 'Не указано',
                    'duration': format_duration(ticket.duration),
                    'date': ticket.issued_at.strftime('%Y-%m-%d'),
                }
                for ticket in tickets
            ]
            return JsonResponse({'data': data}, status=200)

    return JsonResponse({'error': 'Некорректный запрос'}, status=400)