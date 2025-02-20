const GoalManager = {
  init: function () {
    this.bindEvents();
  },

  bindEvents: function () {
    $(document).ready(() => {
      this.handleProgressUpdate();
      this.handleDepositModal();
      this.handleDeleteGoal();
      this.handleAddEditGoalModal();
      this.handleGoalFormSubmit();
      this.handleColorSelection();
    });
  },

  handleProgressUpdate: function () {
    const goals = document.querySelectorAll(".circular-progress-container");

    goals.forEach((goalElement) => {
      const totalGoal = parseFloat(goalElement.getAttribute("data-goal-total"));
      const totalSaved = parseFloat(
        goalElement.getAttribute("data-goal-saved")
      );

      const percent = (totalSaved / totalGoal) * 100;

      this.updateProgress(goalElement, percent, totalGoal);
    });
  },

  updateProgress: function (goalElement, percent, totalGoal) {
    const circle = goalElement.querySelector(".progress-ring__circle--value");
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    const offset = circumference - circumference * (percent / 100);

    circle.style.strokeDashoffset = offset;

    goalElement.querySelector(
      ".progress-value"
    ).textContent = `${percent.toFixed(0)}%`;
  },

  handleDepositModal: function () {
    const depositButtons = document.querySelectorAll(".depositButton");
    const depositModal = new bootstrap.Modal(
      document.getElementById("depositModal")
    );
    const goalNameElement = document.getElementById("goalName");
    const goalColorCircle = document.getElementById("goalColorCircle");
    const depositAmountInput = document.getElementById("depositAmount");
    const depositDateInput = document.getElementById("depositDate");
    const depositNotesInput = document.getElementById("depositNotes");
    const saveDepositButton = document.getElementById("saveDepositButton");

    depositButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const goalName = button.getAttribute("data-goal-name");
        const goalColor = button.getAttribute("data-goal-color");

        goalNameElement.textContent = goalName;
        goalColorCircle.style.backgroundColor = goalColor;

        depositAmountInput.value = "";
        depositDateInput.value = "";
        depositNotesInput.value = "";

        depositModal.show();
      });
    });

    saveDepositButton.addEventListener("click", function () {
      const depositAmount = depositAmountInput.value;
      const depositDate = depositDateInput.value;
      const depositNotes = depositNotesInput.value;

      console.log("Depósito realizado:");
      console.log("Valor:", depositAmount);
      console.log("Data:", depositDate);
      console.log("Notas:", depositNotes);

      depositModal.hide();
    });
  },

  handleDeleteGoal: function () {
    document.querySelectorAll('[id^="delete-goal-"]').forEach((button) => {
      button.addEventListener("click", function () {
        const url = $(this).data("url");
        const itemName = $(this).data("goal-name");

        swal({
          title: "Excluir essa meta?",
          text: `Você tem certeza que deseja desistir da meta '${itemName}'?`,
          buttons: {
            cancel: {
              text: "Cancelar",
              visible: true,
              className: "btn btn-secondary",
            },
            confirm: {
              text: "Excluir",
              className: "btn btn-primary",
            },
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
                    title: "Meta Removida!",
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
    });
  },

  handleAddEditGoalModal: function () {
    const editGoalButtons = document.querySelectorAll(".edit-goal-button");
    editGoalButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const url = button.getAttribute("data-url");
        var modal = $("#editModal");

        fetch(url, {
            method: "GET",
            headers: { "X-Requested-With": "XMLHttpRequest" },
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                modal.find("#goal-name").val(data.goal.name);
                modal.find("#initial-balance").val(data.goal.initial_balance);
                modal.find("#goal-amount").val(data.goal.goal);
                modal.find("#goal-date").val(data.goal.target_at);
                modal.find("#goal-motivation").val(data.goal.motivation);

                modal.find("#goalColorEditInput").val(data.goal.color);
                modal.find("#colorPickerEdit").css("background-color", data.goal.color);

                console.log(url);
                modal.find("#editForm").attr("action", url);
                modal.modal("show");
              } else {
                alert("Erro ao carregar os dados da conta");
              }
            })
            .catch((error) => console.error("Erro:", error));

        
      });
    });
  },

  handleGoalFormSubmit: function () {
    document
      .getElementById("createForm")
      .addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(event.target);
        let url = event.target.action;

        fetch(url, {
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
      });
  },

  handleColorSelection: function () {
    const categoryColorInput = document.getElementById("goal-color");
    const colorPicker = document.getElementById("colorPicker");

    categoryColorInput.addEventListener("input", function () {
      const color = categoryColorInput.value;
      colorPicker.style.backgroundColor = color;
    });

    colorPicker.addEventListener("click", function () {
      categoryColorInput.click();
    });

    const editColorInput = document.getElementById("goalColorEditInput");
    const editcolorPicker = document.getElementById("colorPickerEdit");

    editColorInput.addEventListener("input", function () {
      const color = editColorInput.value;
      editcolorPicker.style.backgroundColor = color;
    });

    editcolorPicker.addEventListener("click", function () {
      editColorInput.click();
    });
  },
};

GoalManager.init();
