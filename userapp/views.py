from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Category, SubCategory
import win32print
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('DejaVu', r'D:\projects\equeue\equeue\fonts\DejaVuSans.ttf'))


def index(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'userapp/index.html', {'categories': categories})


def print_ticket_via_windows(ticket_path):
    if os.path.exists(ticket_path):
        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket Print Job", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            with open(ticket_path, "rb") as f:
                win32print.WritePrinter(hPrinter, f.read())
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    else:
        print("Файл не найден:", ticket_path)


def generate_pdf(ticket_number, category_name):
    save_path = f"D:\\projects\\Tickets\\Ticket_{ticket_number}.pdf"
    doc = SimpleDocTemplate(save_path, pagesize=letter)

    # Создание стиля с уникальным именем
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(name='CustomNormal', fontName='DejaVu', fontSize=12)

    story = []
    story.append(Paragraph("Ваш талон", custom_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Номер талона: <strong>{ticket_number}</strong>", custom_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Категория: <strong>{category_name}</strong>", custom_style))
    story.append(Spacer(1, 12))

    doc.build(story)
    return save_path


def create_ticket(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')
        subcategory = SubCategory.objects.get(id=subcategory_id)
        last_ticket = Ticket.objects.filter(subcategory=subcategory).order_by('issued_at').last()
        last_number = int(last_ticket.number[1:]) if last_ticket else 0
        new_number = last_number + 1
        ticket_number = f"{subcategory.letter}{new_number}"

        ticket = Ticket.objects.create(number=ticket_number, subcategory=subcategory)

        pdf_path = generate_pdf(ticket.number, subcategory.name)
        print_ticket_via_windows(pdf_path)

        return render(request, 'userapp/ticket_print.html',
                      {'ticket_number': ticket.number, 'category_name': subcategory.name})
    else:
        return redirect('category_list')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'userapp/category_list.html', {'categories': categories})


def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    return render(request, 'userapp/subcategory_list.html', {
        'category': category,
        'subcategories': subcategories
    })
