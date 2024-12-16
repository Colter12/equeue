from django.shortcuts import render
from userapp.models import Ticket


def index(request):
    tickets = Ticket.objects.filter(is_served=False, operator__isnull=False).order_by('issued_at')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'infoboard/index_content.html', {'tickets': tickets})

    return render(request, 'infoboard/index.html', {'tickets': tickets})
