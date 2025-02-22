const handleSubmitForm = (form) => {
    form.preventDefault();

    const formData = new FormData(form.target);

    fetch(form.target.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                location.reload(true);
            } else {
                alert("Erro ao criar cartão de crédito: " + JSON.stringify(data.errors));
            }
        })
        .catch((error) => console.error("Erro:", error));
};

const CreditCardManager = {
    init: function () {
        this.bindEvents();
    },

    bindEvents: function () {
        document.addEventListener('DOMContentLoaded', () => {
            this.handleDeleteCreditCard();
            this.handleEditCreditCardModal();
            this.handleRegisterPayment();
            this.handleAddExpense();
            this.handleProgressBars();
            this.handleCardAccessibility();
            this.handleSaveCreditCard();
            this.handleAddCreditCard();
            this.handleChangeTransactionType();
        });
    },

    handleDeleteCreditCard: function () {
        $(document).on("click", '[id^="delete-credit-card-"]', function () {
            const url = $(this).data("url");
            const itemName = $(this).data("item-name");

            swal({
                title: "Excluir esse cartão de crédito?",
                text: `Ao apagar o cartão de crédito "${itemName}", todas as transações e informações vinculadas a ele também serão apagadas. Esta ação não pode ser desfeita!`,
                buttons: {
                    cancel: { text: "Cancelar", visible: true, className: "btn btn-secondary" },
                    confirm: { text: "Excluir", className: "btn btn-primary" },
                },
            }).then(shouldDelete => {
                if (shouldDelete && url) {
                    fetch(url, {
                        method: "DELETE",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                    })
                        .then(response => response.json())
                        .then(data => {
                            swal({
                                title: data.success ? "Deletado!" : "Erro!",
                                text: data.message,
                                icon: data.success ? "success" : "error",
                                buttons: { confirm: { className: data.success ? "btn btn-success" : "btn btn-danger" } },
                            }).then(() => {
                                if (data.success) location.reload();
                            });
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });
        });

        // document.querySelectorAll('[id^="delete-credit-card-"]').forEach(button => {
        //     button.addEventListener('click', function () {
        //         const itemId = this.getAttribute('data-id');
        //         const itemName = this.getAttribute('data-name');

        //         swal({
        //             title: 'Excluir esse cartão?',
        //             text: `Todas as transações relacionadas ao cartão "${itemName}" serão removidas.`,
        //             buttons: {
        //                 cancel: {
        //                     text: 'Cancelar',
        //                     visible: true,
        //                     className: 'btn btn-secondary'
        //                 },
        //                 confirm: {
        //                     text: 'Excluir',
        //                     className: 'btn btn-primary'
        //                 }
        //             }
        //         }).then((Delete) => {
        //             if (Delete) {
        //                 swal({
        //                     title: 'Cartão Deletado!',
        //                     icon: 'success',
        //                     buttons: {
        //                         confirm: {
        //                             className: 'btn btn-success'
        //                         }
        //                     }
        //                 }).then(() => {
        //                     document.getElementById(`credit-card-${itemId}`).remove();
        //                     console.log(`Cartão "${itemName}" excluído para "Outros"`);
        //                 });
        //             } else {
        //                 swal.close();
        //             }
        //         });
        //     });
        // });
    },

    handleAddCreditCardModal: function () {
        document.getElementById('add-credit-card').addEventListener('click', function () {
            document.getElementById('addCreditCardForm').reset();

            var addCreditCardModal = document.getElementById("addCreditCardModal");
            var modal = new bootstrap.Modal(addCreditCardModal);
            modal.show();
        });
    },

    handleChangeTransactionType: function () {
        $(document).on("click", '[id^="addExpenseBtn-"]', function () {
            var cardId = $(this).data("card-id").toString(); // Converte para string
            var transactionType = $("#transactionType");
            var creditCardSelect = $("#creditCardSelect");
            var accountFields = $("#accountFields");
            var cardFields = $("#cardFields");

            console.log("Card ID capturado:", cardId); // Debugging

            // Define o valor fixo para 'card'
            transactionType.val("card");

            // Habilita temporariamente para garantir que seja enviado no formulário
            transactionType.prop("disabled", false);

            // Verifica se a opção existe e define o valor
            if (creditCardSelect.find('option[value="' + cardId + '"]').length > 0) {
                creditCardSelect.val(cardId).trigger("change").prop("disabled", false);
                console.log("Valor do select definido:", creditCardSelect.val()); // Debugging
            } else {
                console.warn("Opção não encontrada no select para o ID:", cardId);
            }

            // Garante que os campos corretos estejam visíveis
            cardFields.removeClass("d-none");
            accountFields.addClass("d-none");

            // Antes do envio do formulário, desabilita novamente o select
            $("form").on("submit", function () {
                transactionType.prop("disabled", false);
            });
        });
    },

    handleEditCreditCardModal: function () {
        $(document).on("click", '[id^="edit-credit-card-"]', function () {
            const url = $(this).data("url");
            const modal = $("#editCreditCardModal");

            fetch(url, { method: "GET", headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(data.credit_card.name);
                        modal.find("#inputNameEdit").val(data.credit_card.name);
                        modal.find("#inputLimitEdit").val(data.credit_card.limit);
                        modal.find("#inputAditionalInfoEdit").val(data.credit_card.additional_info);
                        modal.find("#inputBrandEdit").val(data.credit_card.brand);
                        modal.find("#inputClosingDayEdit").val(data.credit_card.closing_day);
                        modal.find("#inputDueDayEdit").val(data.credit_card.due_day);
                        modal.find("#editCreditCardForm").attr("action", url);
                        modal.modal("show");
                    } else {
                        alert("Erro ao carregar os dados da categoria");
                    }
                })
                .catch(error => console.error("Erro:", error));
        });

        const editForm = document.getElementById("editCreditCardForm");
        if (editForm) {
            editForm.addEventListener("submit", event => {
                event.preventDefault();

                fetch(event.target.action, {
                    method: "POST",
                    body: new FormData(event.target),
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            location.reload();
                        } else {
                            alert("Erro ao editar cartão de crédito: " + JSON.stringify(data.errors));
                        }
                    })
                    .catch(error => console.error("Erro:", error));
            });
        }

        // document.querySelectorAll('[id^="edit-credit-card-"]').forEach(button => {
        //     button.addEventListener('click', function () {
        //         const name = button.getAttribute('data-name');
        //         const limit = button.getAttribute('data-limit');
        //         const additionalData = button.getAttribute('data-additional-data');
        //         const brand = button.getAttribute('data-brand');
        //         const closingDay = button.getAttribute('data-closing-day');
        //         const dueDay = button.getAttribute('data-due-day');

        //         document.getElementById('inputNameEdit').value = name;
        //         document.getElementById('inputLimitEdit').value = limit;
        //         document.getElementById('inputAditionalInfoEdit').value = additionalData;
        //         document.getElementById('inputBrandEdit').value = brand;
        //         document.getElementById('inputClosingDayEdit').value = closingDay;
        //         document.getElementById('inputDueDayEdit').value = dueDay;

        //         const modalElement = document.getElementById('editCreditCardModal');
        //         const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
        //         modal.show();
        //     });
        // });
    },

    handleRegisterPayment: function () {
        $(document).on("click", '[id^="#registerPaymentModal-"]', function () {
            const url = $(this).data("url");  // Pega a URL do atributo data-url
            const modalId = $(this).data("bs-target");  // Pega o ID do modal
            const modal = $(modalId);

            // Configura o formulário dentro do modal
            const form = modal.find("form");
            form.attr("action", url);  // Define a ação do formulário com a URL da fatura

            // Adiciona o evento de submit ao formulário
            form.off("submit").on("submit", handleSubmitForm);
        });
    },

    handleAddExpense: function () {
        $("#createTransactionForm").submit(function (e) {
            e.preventDefault(); // Impedir o envio padrão do formulário

            const formData = new FormData(e.target);

            fetch(e.target.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        $('#createModal').modal('hide');

                        swal({
                            title: "Sucesso!",
                            text: data.message,
                            icon: "success",
                            buttons: {
                                confirm: {
                                    className: "btn btn-success",
                                },
                            },
                        }).then(() => {
                            location.reload();
                        });
                    } else {
                        if (data.errors) {
                            let errors = "";
                            for (const key in data.errors) {
                                errors += `${data.errors[key].join(", ")}\n`;
                            }

                            swal({
                                title: "Erro!",
                                text: errors,
                                icon: "error",
                                buttons: {
                                    confirm: {
                                        className: "btn btn-danger",
                                    },
                                },
                            });
                        } else {
                            swal({
                                title: "Erro!",
                                text: data.message,
                                icon: "error",
                                buttons: {
                                    confirm: {
                                        className: "btn btn-danger",
                                    },
                                },
                            });
                        }
                    }
                })
                .catch((error) => console.error("Erro:", error));
        });
    },

    handleProgressBars: function () {
        const progressBars = document.querySelectorAll('.progress-bar');

        progressBars.forEach(bar => {
            const limite = parseFloat(bar.getAttribute('data-limit'));
            const limiteDisponivel = parseFloat(bar.getAttribute('data-outstanding'));
            const percentage = (limiteDisponivel / limite) * 100;

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
    },

    handleAddCreditCard() {
        document.getElementById("addCreditCardForm")?.addEventListener("submit", handleSubmitForm);
    },
};

CreditCardManager.init();