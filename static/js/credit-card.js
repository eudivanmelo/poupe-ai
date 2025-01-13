document.querySelectorAll('[id^="delete-credit-card-"]').forEach((button) => {
    button.addEventListener('click', function () {
        const itemId = this.getAttribute('data-id');
        const itemName = this.getAttribute('data-name');
        swal({
            title: 'Excluir esse cartão?',
            text: `Todas as transações relacionadas ao cartão "${itemName}" serão removidas.`,
            buttons: {
                cancel: {
                    text: 'Cancelar',
                    visible: true,
                    className: 'btn btn-secondary'
                },
                confirm: {
                    text: 'Excluir',
                    className: 'btn btn-primary'
                }
            }
        }).then((Delete) => {
            if (Delete) {
                // Realiza a exclusão
                swal({
                    title: 'Cartão Deletado!',
                    icon: 'success',
                    buttons: {
                        confirm: {
                            className: 'btn btn-success'
                        }
                    }
                }).then(() => {
                    // Atualização no front-end
                    const cardElement = document.getElementById(`credit-card-${itemId}`).remove();
                    console.log(`Cartão "${itemName}" excluido para "Outros"`);
                });
            } else {
                swal.close();
            }
        });
    });
});

document.getElementById('add-credit-card').addEventListener('click', function () {
    const teste = document.getElementById('creditCardModalLabel');
    teste.textContent = 'Adicionar Cartão de Crédito';
    const saveButton = document.getElementById('saveCreditCard');
    saveButton.textContent = 'Salvar Cartão de Crédito';

    bootstrap.Modal.getInstance(document.getElementById('creditCardModal')).show();
});

document.getElementById('registerPaymentSave').addEventListener('click', function () {
    // Obter os valores dos campos do formulário
    const valorPagamento = document.getElementById('valorPagamento').value;
    const dataEfetivacao = document.getElementById('dataEfetivacao').value;
    const contaSelect = document.getElementById('contaSelect').value;
    const documentoAnexo = document.getElementById('documentoAnexo').files[0];

    // Validar os campos (opcional)
    if (!valorPagamento || !dataEfetivacao || !contaSelect || !documentoAnexo) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    // Processar ou enviar os dados
    // Exemplo: Enviar via AJAX ou exibir uma mensagem de sucesso
    alert(`Pagamento de R$ ${valorPagamento} registrado para a conta ${contaSelect}. Documento: ${documentoAnexo.name}`);

    // Fechar o modal após salvar (opcional)
    const modal = bootstrap.Modal.getInstance(document.getElementById('registrarPagamentoModal'));
    modal.hide();
});

document.addEventListener('DOMContentLoaded', function () {
    const addDespesasBtns = document.querySelectorAll('.addExpenseBtn');

    addDespesasBtns.forEach(function (button) {
        button.addEventListener('click', function () {
            const creditCard = button.getAttribute('data-card-id');
            document.getElementById('expenseCreditCard').value = creditCard;

            const modalElement = document.getElementById('expenseModal');
            const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
            modal.show();

        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Seleciona todos os botões de editar no dropdown
    const editButtons = document.querySelectorAll('.edit-card-btn');

    editButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            // Obtém os dados do cartão
            const name = button.getAttribute('data-name');
            const limit = button.getAttribute('data-limit');
            const additionalData = button.getAttribute('data-additional-data');
            const brand = button.getAttribute('data-brand');
            const closingDay = button.getAttribute('data-closing-day');
            const dueDay = button.getAttribute('data-due-day');

            // Preenche os campos do modal com os dados do cartão
            document.getElementById('creditCardName').value = name;
            document.getElementById('creditCardLimit').value = limit;
            document.getElementById('creditCardAdditionalData').value = additionalData;
            document.getElementById('creditCardBrand').value = brand;
            document.getElementById('creditCardClosingDay').value = closingDay;
            document.getElementById('creditCardDueDay').value = dueDay;

            const saveButton = document.getElementById('saveCreditCard');
            saveButton.textContent = 'Salvar Alterações';
            // Altera o título do modal para "Editar Cartão"
            document.getElementById('creditCardModalLabel').textContent = 'Editar Cartão de Crédito';

            // Exibe o modal
            const modalElement = document.getElementById('creditCardModal');
            const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
            modal.show();
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todas as barras de progresso
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(function (bar) {
        // Obtém os valores de limite e limite disponível
        const limite = parseFloat(bar.getAttribute('data-limit'));
        const limiteDisponivel = parseFloat(bar.getAttribute('data-outstanding'));

        // Calcula a porcentagem
        const percentage = ((limite - limiteDisponivel) / limite) * 100;

        // Atualiza a barra de progresso com a porcentagem calculada
        bar.style.width = percentage + '%';
        bar.setAttribute('aria-valuenow', percentage);
    });
});


document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os cartões que seguem o padrão de ID "credit-card-id"
    const cards = document.querySelectorAll('[id^="credit-card-"]');

    cards.forEach(card => {
        const badge = card.querySelector('.badge');
        const link = card.querySelector('a');

        // Verifica se a badge e o link estão presentes antes de manipular
        if (badge && link) {
            // Verifica o texto da badge
            if (badge.textContent.trim() === 'Fechada') {
                link.classList.remove('disabled-link');
                link.removeAttribute('aria-disabled');
            } else {
                link.classList.add('disabled-link');
                link.setAttribute('aria-disabled', 'true');
            }
        }
    });
});

document.getElementById('saveCreditCard').addEventListener('click', function () {
    var description = document.getElementById('description').value;
    var limit = document.getElementById('limit').value;
    var additionalData = document.getElementById('additionalData').value;
    var brand = document.getElementById('brand').value;
    var associatedAccount = document.getElementById('associatedAccount').value;
    var closingDay = document.getElementById('closingDay').value;
    var dueDay = document.getElementById('dueDay').value;

    if (description && limit && currentBill && brand && closingDay && dueDay) {
        // Aqui você pode processar ou salvar os dados, por exemplo, enviar para um servidor via AJAX.
        console.log({
            description,
            limit,
            additionalData,
            brand,
            associatedAccount,
            closingDay,
            dueDay
        });

        // Fechar o modal após salvar
        var modal = new bootstrap.Modal(document.getElementById('creditCardModal'));
        modal.hide();

        // Limpar o formulário
        document.getElementById('creditCardForm').reset();
    } else {
        alert("Por favor, preencha todos os campos obrigatórios.");
    }
});