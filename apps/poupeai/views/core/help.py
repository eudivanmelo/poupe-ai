from django.views.generic import TemplateView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin

class HelpView(PoupeAIMixin, TemplateView):
    template_name = 'poupeai/help_page.html'

    def get_name(self):
        return "help"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Ajuda e Suporte", "url": None},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        faqs = [
            {
                "question": "Como faço para adicionar uma transação?",
                "answer": "Para adicionar uma nova transação, acesse a seção 'Transações' no menu lateral e clique no botão '+'. No modal de cadastro, preencha os campos obrigatórios, como descrição, valor, categoria e data. Depois de inserir as informações, clique em 'Adicionar Transação'. A listagem de transações será atualizada automaticamente."
            },
            {
                "question": "Como posso gerenciar minhas categorias?",
                "answer": "Na seção 'Categorias' do menu lateral, você pode adicionar, editar ou excluir categorias. Basta definir um nome e escolher uma cor para a categoria, facilitando a organização das suas transações."
            },
            {
                "question": "Como adicionar uma nova conta bancária?",
                "answer": "Acesse a seção 'Contas' no menu lateral e clique no botão '+'. Preencha os detalhes, como nome da conta, saldo inicial e descrição, e finalize clicando em 'Adicionar Conta'."
            },
            {
                "question": "Como definir uma meta financeira?",
                "answer": "Na seção 'Minhas Metas', clique no botão '+'. Defina os detalhes da meta, incluindo nome, valor, saldo inicial, data limite, motivação e cor. Você pode acompanhar seu progresso diretamente na seção de metas."
            },
            {
                "question": "Como adicionar um novo cartão de crédito?",
                "answer": "Acesse a seção 'Cartões de Crédito' no menu lateral e clique no botão '+'. Preencha os detalhes do cartão, como nome, limite, descrição, bandeira, data de fechamento e vencimento, e clique em 'Adicionar Cartão'."
            },
            {
                "question": "Como editar meu perfil?",
                "answer": "Clique no ícone do perfil no menu superior e selecione 'Ver Perfil'. Nessa seção, você pode atualizar suas informações pessoais, como nome, data de nascimento, sexo e foto de perfil."
            },
            {
                "question": "Como excluir minha conta?",
                "answer": "Na seção 'Perfil', clique em 'Excluir Conta'. Para concluir a exclusão, será necessário confirmar sua senha."
            }
        ]

        context.update({
            "faqs": faqs
        })

        return context