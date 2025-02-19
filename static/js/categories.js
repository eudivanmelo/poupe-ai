const CategoryManager = {
    init: function () {
        this.bindEvents();
    },

    bindEvents: function () {
        $(document).ready(() => {
            this.handleDeleteCategory();
            this.handleColorSelection();
            this.handleTabChange();
            this.handleAddCategoryModal();
            this.handleEditCategoryModal();
            this.handleDropdownAnimation();
        });
    },

    handleDeleteCategory: function () {
        $('[id^="delete-category-"]').click(function () {
            const itemId = $(this).data('id');
            const itemName = $(this).data('nome');

            swal({
                title: 'Excluir essa categoria?',
                text: `As transações relacionadas à "${itemName}" serão atualizadas para "Outros".`,
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
                        title: 'Categoria Deletada!',
                        text: `Os dados relacionados à categoria "${itemName}" foram movidos para "Outros".`,
                        icon: 'success',
                        buttons: {
                            confirm: {
                                className: 'btn btn-success'
                            }
                        }
                    }).then(() => {
                        $(`#category-${itemId}`).remove();
                        console.log(`Categoria "${itemName}" movida para "Outros"`);
                    });
                } else {
                    swal.close();
                }
            });
        });
    },

    handleColorSelection: function () {
        $('#categoryColor').on('input', function () {
            const color = $(this).val();
            $('#colorPicker').css('background-color', color);
        });

        $('#colorPicker').click(function () {
            $('#categoryColor').click();
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
            const id = $(this).data('id');
            const nome = $(this).data('nome');
            const cor = $(this).data('cor');
            var modal = $('#editCategoryModal');

            modal.find('#nameInput').val(nome);
            modal.find('#colorInput').val(cor);
            modal.find('#colorPicker').css('background-color', cor);

            modal.modal('show');
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
    }
};

CategoryManager.init();