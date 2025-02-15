from django.shortcuts import render
from django.urls import reverse_lazy

def creditcard_view(request):
    credit_cards = [
        {
            "id": 1,
            "limit": 14005.00,
            "outstanding": 12000.00,
            "available": 3500.00,
            "closing_date": "30/10",
            "additional_data": "My additional data1",
            "brand": 1,
            "due_date": "05/11",
            "associated_account": "none",
            "closing_day": "2",
            "due_day": "10",
            "invoice_amount": 0.00,
            "name": "Nubank",
            "status": "Aberta",
        },
        {
            "id": 2,
            "limit": 10000.00,
            "outstanding": 5000.00,
            "available": 5000.00,
            "name": "Banco do Brasil",
            "closing_date": "15/11",
            "additional_data": "My additional data2",
            "brand": 2,
            "due_date": "20/11",
            "associated_account": "none",
            "closing_day": "1",
            "due_day": "5",
            "invoice_amount": 3500.00,
            "status": "Fechada",
        },
    ]

    accounts = [
        {"id": 1, "name": "Conta Corrente"},
        {"id": 2, "name": "Conta Poupança"},
    ]

    categories = [
        {"id": 1, "name": "Aluguel", "valor": 1000.50, "cor": "#ff0000"},
        {"id": 2, "name": "Supermercado", "valor": 500.00, "cor": "#00ff00"},
        {"id": 3, "name": "Transporte", "valor": 150.00, "cor": "#ff6600"},
        {"id": 4, "name": "Internet", "valor": 120.00, "cor": "#00ffff"},
        {"id": 5, "name": "Saúde", "valor": 300.00, "cor": "#ff99cc"},
    ]

    invoices = [
        {"id": 1, "month": "Janeiro", "year": 2025},
        {"id": 2, "month": "Fevereiro", "year": 2025},
        {"id": 3, "month": "Março", "year": 2025},
    ]

    credit_card_brands = [
        {"id": 1, "name": "Visa"},
        {"id": 2, "name": "Mastercard"},
        {"id": 3, "name": "American Express"},
        {"id": 4, "name": "Elo"},
        {"id": 5, "name": "Hipercard"},
        {"id": 6, "name": "Diners Club"},
    ]

    for card in credit_cards:
        card["usage_percentage"] = "{:.1f}".format((card["outstanding"] / card["limit"]) * 100)

    breadcrumbs = [
        {"name": "Dashboard", "url": reverse_lazy('dashboard')},
        {"name": "Cartões de Crédito", "url": None},
    ]

    context = {
        "breadcrumbs": breadcrumbs,
        "credit_cards": credit_cards,
        "categories": categories,
        "accounts": accounts,
        "invoices": invoices,
        "credit_card_brands": credit_card_brands,
        "name": "credit-cards",
    }

    return render(request, 'poupeai/credit_card_page.html', context)