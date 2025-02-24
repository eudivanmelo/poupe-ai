const handleSubmitForm = (form) => {
  form.preventDefault(); // Impedir o envio padrão do formulário

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
        location.reload(); // Atualiza a página para exibir a nova conta
      } else {
        alert("Erro ao criar conta: " + JSON.stringify(data.errors));
      }
    })
    .catch((error) => console.error("Erro:", error));
};

var Modals = (function () {
  var init_buttons = function () {
    $('[id^="detail-account-"]').click(function (e) {
      var url = $(this).data("url");
      var modal = $("#detailModal");

      fetch(url, {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            modal.find("#accountName").text(data.account.name);
            modal.find("#accountDescription").text(data.account.description);
            modal.find("#accountBalance").text(
              `R$ ${Number(data.account.balance).toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
              })}`
            );
            modal
              .find("#accountIncome")
              .text(
                `R$ ${Number(data.account.total_income).toLocaleString(
                  "pt-BR",
                  { minimumFractionDigits: 2 }
                )}`
              );
            modal
              .find("#accountExpense")
              .text(
                `R$ ${Number(data.account.total_expense).toLocaleString(
                  "pt-BR",
                  { minimumFractionDigits: 2 }
                )}`
              );

            let createdAt = new Date(data.account.created_at);

            let dateFormatted = new Intl.DateTimeFormat("pt-BR", {
              day: "2-digit",
              month: "2-digit",
              year: "numeric",
            }).format(createdAt);

            let timeFormatted = new Intl.DateTimeFormat("pt-BR", {
              hour: "2-digit",
              minute: "2-digit",
              hour12: false,
            }).format(createdAt);

            modal
              .find("#accountCreatedAt")
              .text(`${dateFormatted} - ${timeFormatted}`);

            let transactionsContainer = modal.find("#accountTransactions");
            transactionsContainer.empty(); // Limpar transações anteriores

            if (
              data.account.transactions &&
              data.account.transactions.length > 0
            ) {
              // Exibir as últimas 10 transações
              data.account.transactions.slice(0, 10).forEach((transaction) => {
                let transactionDate = new Date(transaction.created_at);
                let transactionHtml = `
                  <li class="list-group-item gap-2 justify-content-between">
                    <strong>${new Intl.DateTimeFormat("pt-BR", {
                      day: "2-digit",
                      month: "2-digit",
                      year: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                      hour12: false,
                    }).format(transactionDate)}</strong>
                    <span>${transaction.description}</span>
                    <span class="${
                      transaction.type == "expense"
                        ? "text-danger"
                        : "text-success"
                    }">
                      R$ ${Number(transaction.amount).toLocaleString("pt-BR", {
                        minimumFractionDigits: 2,
                      })}
                    </span>
                  </li>
                `;
                transactionsContainer.append(transactionHtml);
              });
            } else {
              transactionsContainer.html("<p>Sem transações</p>");
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

    $('[id^="edit-account-"]').click(function (e) {
      var url = $(this).data("url");
      var modal = $("#editModal");

      fetch(url, {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            modal.find("#nameInput").val(data.account.name);
            modal.find("#descriptionInput").val(data.account.description);

            modal.find("#editForm").attr("action", url);
            modal.modal("show");
          } else {
            alert("Erro ao carregar os dados da conta");
          }
        })
        .catch((error) => console.error("Erro:", error));
    });

    $('[id^="delete-account-"]').click(function (e) {
      var url = $(this).data("url");
      var itemName = $(this).data("item-name");

      swal({
        title: "Tem certeza?",
        text: `Ao apagar a conta '${itemName}' todas as transações vinculadas a ela também serão apagadas, este processo não pode ser revertido!`,
        dangerMode: true,
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
            .then((response) => response.json())
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
                  location.reload();
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

    const form = document.getElementById("create-form");
    form.addEventListener("submit", handleSubmitForm);
  };

  return {
    init: function () {
      init_buttons();
    },
  };
})();

jQuery(document).ready(function () {
  Modals.init();
});
