const handleSubmitForm = (form) => {
    form.preventDefault();

    const formData = new FormData(form.target);

    const type = document.querySelector("#categoryTabs .nav-link.active").id.includes("despesas") ? "expense" : "income";
    formData.append("type", type);

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
            location.reload();
        } else {
            alert("Erro ao criar conta: " + JSON.stringify(data.errors));
        }
      })
      .catch((error) => console.error("Erro:", error));
}

const CategoryManager = {
    init: function () {
        this.bindEvents();
    },

    bindEvents: function () {
        $(document).ready(() => {
            this.handleDeleteCategory();
            this.handleColorSelection();
            this.handleTabChange();
            this.handleAddCategory();
            this.handleEditCategoryModal();
            this.handleDropdownAnimation();
        });
    },

    handleDeleteCategory: function () {
        $('[id^="delete-category-"]').click(function () {
            var url = $(this).data("url");
            var itemName = $(this).data("item-name");

            swal({
                title: 'Excluir essa categoria?',
                text: `Ao apagar a categoria "${itemName}" todas as transações vinculadas a ela também serão apagadas. Esta ação não pode ser desfeita!`,
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
                    if (!url) return;
                    
                    fetch(url, {
                        method: "DELETE",
                        headers: {
                          "X-Requested-With": "XMLHttpRequest",
                          "X-CSRFToken": getCookie("csrftoken"),
                        },
                    }).then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            swal({
                                title: 'Deletada!',
                                text: data.message,
                                icon: 'success',
                                buttons: {
                                    confirm: {
                                        className: 'btn btn-success'
                                    }
                                }
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
    },

    handleColorSelection: function () {
        $('#colorInput').on('input', function () {
            const color = $(this).val();
            $('#colorPicker').css('background-color', color);
            $('#colorPickerEdit').css('background-color', color);
        });

        $('#colorInputEdit').on('input', function () {
            const color = $(this).val();
            $('#colorPicker').css('background-color', color);
            $('#colorPickerEdit').css('background-color', color);
        });

        $('#colorPicker').click(function () {
            $('#colorInput').click();
        });

        $('#colorPickerEdit').click(function () {
            $('#colorInputEdit').click();
        });
    },

    handleTabChange: function () {
        $('#categoryTabs .nav-link').on('shown.bs.tab', function (event) {
            const newTotal = $(event.target).data('total');
            const newCatTotal = $(event.target).data('total-cat');
            $('#total-value').text(`R$ ${newTotal}`);
            $('#total-categorias').text(`${newCatTotal}`);
            console.log('Categoria selecionada:', $(event.target).text());
        });
    },

    handleAddCategoryModal: function () {
        $('#add-category').click(function () {

            $('#addCategoryModal').modal('show');
        });
    },

    handleEditCategoryModal: function () {
        $('[id^="edit-category-"]').click(function () {
            var url = $(this).data("url");
            var modal = $("#editCategoryModal");

            fetch(url, {
                method: "GET",
                headers: { "X-Requested-With": "XMLHttpRequest" },
              })
                .then((response) => response.json())
                .then((data) => {
                  if (data.success) {

                    modal.find('#nameInput').val(data.category.name);
                    modal.find('#colorInput').val(data.category.color);
                    modal.find('#colorPickerEdit').css('background-color', data.category.color);
        
                    modal.find("#editCategoryForm").attr("action", url);
                    modal.modal("show");
                  } else {
                    alert("Erro ao carregar os dados da categoria");
                  }
                })
                .catch((error) => console.error("Erro:", error));

            // const id = $(this).data('id');
            // const nome = $(this).data('nome');
            // const cor = $(this).data('cor');
            // var modal = $('#editCategoryModal');

            // modal.find('#nameInput').val(nome);
            // modal.find('#colorInput').val(cor);
            // modal.find('#colorPicker').css('background-color', cor);

            // modal.modal('show');
        });
    },

    handleDropdownAnimation: function () {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.addEventListener('show.bs.dropdown', () => {
                dropdown.closest('.category-card').classList.add('dropdown-open');
            });

            dropdown.addEventListener('hide.bs.dropdown', () => {
                dropdown.closest('.category-card').classList.remove('dropdown-open');
            });
        });
    },

    handleAddCategory: function () {
        const form = document.getElementById("addCategoryForm");
        form.addEventListener("submit", handleSubmitForm);
    }
};

CategoryManager.init();