var Alerts = (function () {
  var init_buttons = function () {
    $('[id^="detail-transaction-"]').click(function (e) {
      var url = $(this).data("url");
      var modal = $("#detailModal");

      fetch(url, {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Erro HTTP! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            const description = data.transaction.description;
            let amount = Number(data.transaction.amount).toLocaleString(
              "pt-BR",
              {
                minimumFractionDigits: 2,
              }
            );

            if (data.transaction.type === "card") {
              amount = Number(
                data.transaction.installments_total_amount
              ).toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
              });
            }

            const typeMap = {
              card: "Cartão de Crédito",
              expense: "Despesa",
              income: "Receita",
            };

            const type = typeMap[data.transaction.type] || "Receita";
            const category = data.transaction.category;

            html = `<li class="list-group-item gap-2">
                      <strong>Descrição:</strong>
                      <span>${description}</span>
                    </li>
                    <li class="list-group-item gap-2">
                      <strong>Valor:</strong>
                      <span>R$ ${amount}</span>
                    </li>
                    <li class="list-group-item gap-2">
                      <strong>Tipo:</strong>
                      <span>${type}</span>
                    </li>
                    <li class="list-group-item gap-2">
                      <strong>Categoria:</strong>
                      <span>${category}</span>
                    </li>
                    `;

            if (data.transaction.type === "card") {
              const card_transaction = data.transaction.card_transaction;
              const paymentDate = new Date(data.transaction.payment_at);

              const paymentDateFormatted = new Intl.DateTimeFormat("pt-BR", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
              }).format(paymentDate);

              const installmentValue = Number(
                data.transaction.amount
              ).toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
              });

              html += `<li class="list-group-item gap-2">
                          <strong>Parcelas:</strong>
                          <span>${data.transaction.total_installments}</span>
                        </li>
                        <li class="list-group-item gap-2">
                          <strong>Valor da Parcela:</strong>
                          <span>R$ ${installmentValue}</span>
                        </li>
                        <li class="list-group-item gap-2">
                          <strong>Data de Pagamento:</strong>
                          <span>${paymentDateFormatted}</span>
                        </li>
                        <li class="list-group-item gap-2">
                          <strong>Cartão de Crédito:</strong>
                          <span>${data.transaction.credit_card}</span>
                        </li>`;
            } else {
              const acc_transaction = data.transaction.account_transaction;
              let paymentDateFormatted = "";
              if (data.transaction.payment_at) {
                const paymentDate = new Date(data.transaction.payment_at);

                paymentDateFormatted = new Intl.DateTimeFormat("pt-BR", {
                  day: "2-digit",
                  month: "2-digit",
                  year: "numeric",
                }).format(paymentDate);
              } else {
                const statusMap = {
                  paid: "Pago",
                  unpaid: "Aguardando Pagamento",
                  warning: "Proximo de Vencer",
                  expired: "Vencida",
                };
                paymentDateFormatted = statusMap[data.transaction.status];
              }

              const expireDate = new Date(acc_transaction.expire_at);

              const expireDateFormatted = new Intl.DateTimeFormat("pt-BR", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
              }).format(expireDate);

              html += `<li class="list-group-item gap-2">
                        <strong>Data de Pagamento:</strong>
                        <span>${paymentDateFormatted}</span>
                      </li>
                      <li class="list-group-item gap-2">
                        <strong>Data de Vencimento:</strong>
                        <span>${expireDateFormatted}</span>
                      </li>
                      <li class="list-group-item gap-2">
                        <strong>Conta:</strong>
                        <span>${acc_transaction.account}</span>
                      </li>`;
            }

            modal.find("#transaction-details").html(html);

            if (data.transaction.image) {
              modal
                .find("#attachment")
                .html(
                  `<img src="${data.transaction.image}" alt="Anexo da transação" />`
                );
            } else {
              modal
                .find("#attachment")
                .html(`<p>Nenhum comprovante de pagamento informado!</p>`);
            }
          } else {
            swal({
              title: "Erro!",
              text: "Erro ao buscar detalhes da conta!",
              icon: "error",
              buttons: {
                confirm: {
                  className: "btn btn-danger",
                },
              },
            });
          }
        })
        .catch((error) => console.error("Erro:", error));

      modal.modal("show");
    });

    $('[id^="edit-transaction-"]').click(function (e) {
      var url = $(this).data("url");
      var modal = $("#editModal");

      fetch(url, {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            modal.find("#editDescriptionInput").val(data.transaction.description);
            modal.find("#editValueInput").val(data.transaction.amount);
            modal.find("#editPaymentDateInput").val(new Date(data.transaction.payment_at).toISOString().split('T')[0]);
            modal.find("#editCategoryInput").val(data.transaction.category);

            if (data.transaction.type === "card") {
              modal.find("#editTransactionType").val('card').change();
              modal.find("#editCreditCardSelect").val(data.transaction.credit_card);
              modal.find("#editInstallmentsInput").val(data.transaction.installments);
            }
            else {
              modal.find("#editTransactionType").val('account').change();
              modal.find("#editAccountInput").val(data.transaction.account);
              modal.find("#editExpirationDateInput").val(data.transaction.expire_at);
            }

            modal.find("#editTransactionForm").attr("action", url);
            modal.modal("show");
          } else {
            alert("Erro ao carregar os dados da conta");
          }
        })
        .catch((error) => console.error("Erro:", error));
    });

    $('[id^="delete-transaction-"]').click(function (e) {
      var itemName = $(this).data("item-name");
      var url = $(this).data("url");

      swal({
        title: "Tem certeza?",
        text: `Ao apagar a transação '${itemName}' você não poderá reverter isso!`,
        type: "warning",
        buttons: {
          cancel: { text: "Cancelar", visible: true, className: "btn btn-secondary" },
          confirm: { text: "Excluir", className: "btn btn-primary" },
        },
      }).then((Delete) => {
        if (Delete) {
          if (!url) return;

          fetch(url, {
            method: "DELETE",
            headers: {
              "X-Requested-With": "XMLHttpRequest",
              "X-CSRFToken": getCookie("csrftoken"),
            },
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}`);
              }
              return response.json();
            })
            .then((data) => {
              if (data.success) {
                swal({
                  title: "Deletado!",
                  text: data.message,
                  icon: "success",
                  buttons: {
                    confirm: {
                      className: "btn btn-success",
                    },
                  },
                }).then(() => {
                  location.reload(true);
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
            })
            .catch((error) => console.error("Erro:", error));
        } else {
          swal.close();
        }
      });
    });

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
              location.reload(true);
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
  };

  return {
    init: function () {
      init_buttons();
    },
  };
})();

jQuery(document).ready(function () {
  Alerts.init();

  $("#transactionType").change(function () {
    var type = $(this).val();
    var cardFields = $("#cardFields");
    var accountFields = $("#accountFields");

    if (type === "card") {
      cardFields.removeClass("d-none");
      accountFields.addClass("d-none");
    } else {
      cardFields.addClass("d-none");
      accountFields.removeClass("d-none");
    }
  });

  $("#editTransactionType").change(function () {
    var type = $(this).val();
    var cardFields = $("#editCardFields");
    var accountFields = $("#editAccountFields");

    if (type === "card") {
      cardFields.removeClass("d-none");
      accountFields.addClass("d-none");
    } else {
      cardFields.addClass("d-none");
      accountFields.removeClass("d-none");
    }
  });


});
