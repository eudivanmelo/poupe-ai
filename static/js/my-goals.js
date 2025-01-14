document.addEventListener('DOMContentLoaded', function () {
    const goals = document.querySelectorAll('.circular-progress-container');

    goals.forEach(goalElement => {
        const totalGoal = parseFloat(goalElement.getAttribute('data-goal-total'));
        const totalSaved = parseFloat(goalElement.getAttribute('data-goal-saved'));
        const color = goalElement.getAttribute('data-goal-color');

        const percent = (totalSaved / totalGoal) * 100;

        updateProgress(goalElement, percent, totalGoal, totalSaved, color);
    });

    function updateProgress(goalElement, percent, totalGoal, totalSaved, color) {
        const circle = goalElement.querySelector('.progress-ring__circle--value');
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;

        const offset = circumference - (circumference * (percent / 100));

        circle.style.strokeDashoffset = offset;

        goalElement.querySelector('.progress-value').textContent = `${percent.toFixed(0)}%`;

        const investedAmount = totalGoal * (percent / 100);
        const remainingAmount = totalGoal - investedAmount;

        const investedAmountElement = goalElement.querySelector(`#investedAmount-${goalElement.getAttribute('data-goal-id')}`);
        investedAmountElement.textContent = `R$ ${investedAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

        const remainingAmountElement = goalElement.querySelector(`#remainingAmount-${goalElement.getAttribute('data-goal-id')}`);
        remainingAmountElement.textContent = `R$ ${remainingAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const depositButtons = document.querySelectorAll('.depositButton');
    const depositModal = new bootstrap.Modal(document.getElementById('depositModal'));
    const goalNameElement = document.getElementById('goalName');
    const goalColorCircle = document.getElementById('goalColorCircle');
    const depositAmountInput = document.getElementById('depositAmount');
    const depositDateInput = document.getElementById('depositDate');
    const depositNotesInput = document.getElementById('depositNotes');
    const saveDepositButton = document.getElementById('saveDepositButton');

    depositButtons.forEach(button => {
        button.addEventListener('click', function () {
            const goalName = button.getAttribute('data-goal-name');
            const goalColor = button.getAttribute('data-goal-color');

            goalNameElement.textContent = goalName;
            goalColorCircle.style.backgroundColor = goalColor;

            depositAmountInput.value = '';
            depositDateInput.value = '';
            depositNotesInput.value = '';

            depositModal.show();
        });
    });

    saveDepositButton.addEventListener('click', function () {
        const depositAmount = depositAmountInput.value;
        const depositDate = depositDateInput.value;
        const depositNotes = depositNotesInput.value;

        console.log("Depósito realizado:");
        console.log("Valor:", depositAmount);
        console.log("Data:", depositDate);
        console.log("Notas:", depositNotes);

        depositModal.hide();
    });
});


document.querySelectorAll('[id^="delete-goal-"]').forEach((button) => {
    button.addEventListener('click', function () {
        const itemId = this.getAttribute('data-goal-id');
        const itemName = this.getAttribute('data-goal-name');
        swal({
            title: 'Excluir essa meta?',
            text: `Você tem certeza que deseja desistir dessa meta?`,
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
                    title: 'Meta Removida!',
                    icon: 'success',
                    buttons: {
                        confirm: {
                            className: 'btn btn-success'
                        }
                    }
                }).then(() => {
                    document.getElementById(`my-goal-${itemId}`).remove();
                    console.log(`Cartão "${itemName}" excluido para "Outros"`);
                });
            } else {
                swal.close();
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const addGoalButton = document.getElementById('add-goal');

    const modal = document.getElementById('myGoalModal');
    const modalTitle = document.getElementById('myGoalModalLabel');
    const saveGoalButton = document.getElementById('saveGoalButton');
    const goalNameInput = document.getElementById('goal-name');
    const goalBalanceInput = document.getElementById('initial-balance');
    const goalAmountInput = document.getElementById('goal-amount');
    const goalDateInput = document.getElementById('goal-date');
    const goalMotivationInput = document.getElementById('goal-motivation');
    const goalColorInput = document.getElementById('goal-color');

    addGoalButton.addEventListener('click', function () {
        modalTitle.textContent = 'Adicionar Meta';
        saveGoalButton.textContent = 'Salvar Meta';

        goalNameInput.value = '';
        goalBalanceInput.value = '';
        goalAmountInput.value = '';
        goalDateInput.value = '';
        goalMotivationInput.value = '';
        goalColorInput.value = '#000000';
        const colorPicker = document.getElementById('colorPicker');
        colorPicker.style.backgroundColor = '#000000';
    });

    const editGoalButtons = document.querySelectorAll('.edit-goal-button');
    editGoalButtons.forEach(button => {
        button.addEventListener('click', function () {

            const goalName = button.getAttribute('data-goal-name');
            const goalBalance = button.getAttribute('data-goal-balance');
            const goalAmount = button.getAttribute('data-goal-amount');
            const goalDate = button.getAttribute('data-goal-date');
            const goalMotivation = button.getAttribute('data-goal-motivation');
            const goalColor = button.getAttribute('data-goal-color');

            modalTitle.textContent = 'Editar Meta';
            saveGoalButton.textContent = 'Salvar Alterações';

            goalNameInput.value = goalName;
            goalBalanceInput.value = goalBalance;
            goalAmountInput.value = goalAmount;
            goalDateInput.value = goalDate;
            goalMotivationInput.value = goalMotivation;
            goalColorInput.value = goalColor;
            const colorPicker = document.getElementById('colorPicker');
            colorPicker.style.backgroundColor = goalColor;

            const modalElement = document.getElementById('myGoalModal');
            const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
            modal.show();
        });
    });
});

document.getElementById('goal-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const goalName = document.getElementById('goal-name').value;
    const initialBalance = document.getElementById('initial-balance').value;
    const goalAmount = document.getElementById('goal-amount').value;
    const goalDate = document.getElementById('goal-date').value;
    const goalMotivation = document.getElementById('goal-motivation').value;
    const goalColor = document.getElementById('goal-color').value;

    console.log({
        goalName,
        initialBalance,
        goalAmount,
        goalDate,
        goalMotivation,
        goalColor
    });

    var modal = bootstrap.Modal.getInstance(document.getElementById('myGoalModal'));
    modal.hide();
});

const categoryColorInput = document.getElementById('goal-color');
const colorPicker = document.getElementById('colorPicker');

categoryColorInput.addEventListener('input', function () {
    const color = categoryColorInput.value;
    colorPicker.style.backgroundColor = color;
});

colorPicker.addEventListener('click', function () {
    categoryColorInput.click();
});