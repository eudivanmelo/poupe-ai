const CreditCardManager = {
    init: function () {
        this.bindEvents();
    },

    bindEvents: function () {
        document.addEventListener('DOMContentLoaded', () => {
            this.handleDeleteCreditCard();
            this.handleAddCreditCardModal();
            this.handleEditCreditCardModal();
            this.handleRegisterPayment();
            this.handleAddExpense();
            this.handleProgressBars();
            this.handleCardAccessibility();
            this.handleSaveCreditCard();
        });
    },

    handleDeleteCreditCard: function () {
        document.querySelectorAll('[id^="delete-credit-card-"]').forEach(button => {
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
                        swal({
                            title: 'Cartão Deletado!',
                            icon: 'success',
                            buttons: {
                                confirm: {
                                    className: 'btn btn-success'
                                }
                            }
                        }).then(() => {
                            document.getElementById(`credit-card-${itemId}`).remove();
                            console.log(`Cartão "${itemName}" excluído para "Outros"`);
                        });
                    } else {
                        swal.close();
                    }
                });
            });
        });
    },

    handleAddCreditCardModal: function () {
        document.getElementById('add-credit-card').addEventListener('click', function () {
            document.getElementById('creditCardForm').reset();
            
            document.getElementById('creditCardModalLabel').textContent = 'Adicionar Cartão de Crédito';
            document.getElementById('saveCreditCard').textContent = 'Salvar Cartão de Crédito';

            bootstrap.Modal.getInstance(document.getElementById('creditCardModal')).show();
        });
    },

    handleEditCreditCardModal: function () {
        document.querySelectorAll('.edit-card-btn').forEach(button => {
            button.addEventListener('click', function () {
                const name = button.getAttribute('data-name');
                const limit = button.getAttribute('data-limit');
                const additionalData = button.getAttribute('data-additional-data');
                const brand = button.getAttribute('data-brand');
                const closingDay = button.getAttribute('data-closing-day');
                const dueDay = button.getAttribute('data-due-day');

                document.getElementById('creditCardName').value = name;
                document.getElementById('creditCardLimit').value = limit;
                document.getElementById('creditCardAdditionalData').value = additionalData;
                document.getElementById('creditCardBrand').value = brand;
                document.getElementById('creditCardClosingDay').value = closingDay;
                document.getElementById('creditCardDueDay').value = dueDay;

                document.getElementById('creditCardModalLabel').textContent = 'Editar Cartão de Crédito';
                document.getElementById('saveCreditCard').textContent = 'Salvar Alterações';

                const modalElement = document.getElementById('creditCardModal');
                const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
                modal.show();
            });
        });
    },

    handleRegisterPayment: function () {
        document.getElementById('registerPaymentSave').addEventListener('click', function () {
            const valorPagamento = document.getElementById('valorPagamento').value;
            const dataEfetivacao = document.getElementById('dataEfetivacao').value;
            const contaSelect = document.getElementById('contaSelect').value;
            const documentoAnexo = document.getElementById('documentoAnexo').files[0];

            if (!valorPagamento || !dataEfetivacao || !contaSelect || !documentoAnexo) {
                alert("Por favor, preencha todos os campos.");
                return;
            }

            alert(`Pagamento de R$ ${valorPagamento} registrado para a conta ${contaSelect}. Documento: ${documentoAnexo.name}`);

            const modal = bootstrap.Modal.getInstance(document.getElementById('registrarPagamentoModal'));
            modal.hide();
        });
    },

    handleAddExpense: function () {
        document.querySelectorAll('.addExpenseBtn').forEach(button => {
            button.addEventListener('click', function () {
                const creditCard = button.getAttribute('data-card-id');
                document.getElementById('expenseCreditCard').value = creditCard;

                const modalElement = document.getElementById('expenseModal');
                const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
                modal.show();
            });
        });
    },

    handleProgressBars: function () {
        const progressBars = document.querySelectorAll('.progress-bar');

        progressBars.forEach(bar => {
            const limite = parseFloat(bar.getAttribute('data-limit'));
            const limiteDisponivel = parseFloat(bar.getAttribute('data-outstanding'));
            const percentage = ((limite - limiteDisponivel) / limite) * 100;

            bar.style.width = percentage + '%';
            bar.setAttribute('aria-valuenow', percentage);
        });
    },

    handleCardAccessibility: function () {
        document.querySelectorAll('[id^="credit-card-"]').forEach(card => {
            const badge = card.querySelector('.badge');
            const link = card.querySelector('a');

            if (badge && link) {
                if (badge.textContent.trim() === 'Fechada') {
                    link.classList.remove('disabled-link');
                    link.removeAttribute('aria-disabled');
                } else {
                    link.classList.add('disabled-link');
                    link.setAttribute('aria-disabled', 'true');
                }
            }
        });
    },

    handleSaveCreditCard: function () {
        document.getElementById('saveCreditCard').addEventListener('click', function () {
            const description = document.getElementById('description').value;
            const limit = document.getElementById('limit').value;
            const additionalData = document.getElementById('additionalData').value;
            const brand = document.getElementById('brand').value;
            const associatedAccount = document.getElementById('associatedAccount').value;
            const closingDay = document.getElementById('closingDay').value;
            const dueDay = document.getElementById('dueDay').value;

            if (description && limit && brand && closingDay && dueDay) {
                console.log({
                    description,
                    limit,
                    additionalData,
                    brand,
                    associatedAccount,
                    closingDay,
                    dueDay
                });

                const modal = new bootstrap.Modal(document.getElementById('creditCardModal'));
                modal.hide();
                document.getElementById('creditCardForm').reset();
            } else {
                alert("Por favor, preencha todos os campos obrigatórios.");
            }
        });
    }
};

CreditCardManager.init();