var Elements = (function () {
  var myBalanceAnalyticsChart, myCardsAnalyticsChart, myCategoryChart;

  var init_balanceAnalyticsChart = function () {
    var balanceAnalyticsChart = $("#balance-analytics-chart");
    const url = balanceAnalyticsChart.data("url");

    $.ajax({
      url: url,
      method: "GET",
      success: function (response) {
        myBalanceAnalyticsChart = new Chart(balanceAnalyticsChart, {
          type: "line",
          data: response,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
              position: "top",
            },
            tooltips: {
              callbacks: {
                label: function (tooltipItem, data) {
                  var value = tooltipItem.yLabel;
                  return (
                    "R$ " +
                    value.toLocaleString("pt-BR", {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                  );
                },
              },
              bodySpacing: 4,
              mode: "nearest",
              intersect: 0,
              position: "nearest",
              xPadding: 10,
              yPadding: 10,
              caretPadding: 10,
            },
            layout: {
              padding: { left: 15, right: 15, top: 15, bottom: 15 },
            },
          },
        });
      },
      error: function () {
        console.error("Erro ao carregar os dados do gráfico.");
      },
    });
  };

  var init_cardsAnalyticsChart = function () {
    var cardsAnalyticsChart = $("#cards-analytics-chart");
    const url = cardsAnalyticsChart.data("url");

    $.ajax({
      url: url,
      method: "GET",
      success: function (response) {
        myCardsAnalyticsChart = new Chart(cardsAnalyticsChart, {
          type: "bar",
          data: response, // Usa os dados retornados pela view
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true,
                  },
                },
              ],
            },
          },
        });
      },
      error: function () {
        console.error("Erro ao carregar os dados do gráfico.");
      },
    });
  };

  var init_categoryChart = function () {
    var categoryChart = $("#category-chart");
    const url = categoryChart.data("url");

    $.ajax({
      url: url,
      method: "GET",
      success: function (response) {
        myCategoryChart = new Chart(categoryChart, {
          type: "pie",
          data: response, // Usa os dados retornados pela view
          options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
              position: "bottom",
              labels: {
                fontColor: "rgb(154, 154, 154)",
                fontSize: 11,
                usePointStyle: true,
                padding: 20,
              },
            },
            pieceLabel: {
              render: "percentage",
              fontColor: "white",
              fontSize: 14,
            },
            tooltips: false,
            layout: {
              padding: {
                left: 20,
                right: 20,
                top: 20,
                bottom: 20,
              },
            },
          },
        });
      },
      error: function () {
        console.error("Erro ao carregar os dados do gráfico.");
      },
    });
  };

  // Adicionar evento de resize para todos os gráficos
  $(window).on("resize", function () {
    if (myBalanceAnalyticsChart) myBalanceAnalyticsChart.resize();
    if (myCardsAnalyticsChart) myCardsAnalyticsChart.resize();
    if (myCategoryChart) myCategoryChart.resize();
  });

  return {
    init: function () {
      init_balanceAnalyticsChart();
      init_cardsAnalyticsChart();
      init_categoryChart();
    },
  };
})();

const LoadTip = function () {
  var content = $("#iaTips");
  var url = content.data("url");

  fetch(url, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        content.html(data.message);
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
};

jQuery(document).ready(function () {
  Elements.init();

  LoadTip();
  $("#iaTipButton").click(function () {
    LoadTip();
  });

  $("#reportIaButton").click(function () {
    const modal = $("#reportIaModal");
    const url = $(this).data("url");

    fetch(url, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          modal.find(".modal-body").html(data.message);

          modal.modal("show");
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
  });

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
          $("#createModal").modal("hide");

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
});
