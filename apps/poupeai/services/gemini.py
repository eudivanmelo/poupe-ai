import google.generativeai as genai
from django.conf import settings

# Configura a API do Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

def generate_text(prompt):
    """Gera um texto usando a API Gemini"""
    model = genai.GenerativeModel("gemini-1.5-flash") 
    response = model.generate_content(prompt)
    
    return response.text if response else "Erro ao gerar resposta"

def generate_financial_summary(data):
    """
    Envia um prompt para o Gemini e retorna a resposta formatada como HTML.
    """
    prompt = f'Gere um relatório financeiro com base nos dados a seguir e em formato html, retorne apenas o html que contenha informações sobre o financeiro do usuário e com dicas de como pode melhorar, não precisa listar todas as transações, apenas as que achar relevantes e nas transações, não precisar colocar o tipo, mas considere o tipo em relação ao valor(amount), e se não houver data de pagamento, coloque como "Não pago":\n\n'
    prompt += f'Total de renda: {data["total_income"]}\n'
    prompt += f'Total de despesas: {data["total_expenses"]}\n'
    prompt += f'Saldo atual: {data["current_balance"]}\n'
    prompt += f'Categoria de maior gasto: {data["highest_expense_category"]}\n'
    prompt += f'Total gasto na categoria: {data["total_category_expense"]}\n'
    prompt += f'Porcentagem do total de despesas: {data["category_percentage"]}\n\n'
    prompt += 'Transações:\n'
    for transaction in data["transactions"]:
        prompt += f'{transaction["date"]} - {transaction["description"]} - {transaction["category"]} - {transaction["amount"]} - {transaction["type"]}\n'
        
    prompt += '\n\n'
    
    response = generate_text(prompt)
    return response

def tip(data):
    """
    Envia um prompt para o Gemini e retorna a resposta formatada como HTML.
    """
    prompt = f'Gere um dica com até 3 parágrafos com base nos dados a seguir e em formato html, retorne apenas o html que contenha essa dica:\n\n'
    prompt += f'Total de renda: {data["total_income"]}\n'
    prompt += f'Total de despesas: {data["total_expenses"]}\n'
    prompt += f'Saldo atual: {data["current_balance"]}\n'
    prompt += 'Transações:\n'
    for transaction in data["transactions"]:
        prompt += f'{transaction["date"]} - {transaction["description"]} - {transaction["category"]} - {transaction["amount"]} - {transaction["type"]}\n'
        
    prompt += '\n\n'
    
    response = generate_text(prompt)
    return response
