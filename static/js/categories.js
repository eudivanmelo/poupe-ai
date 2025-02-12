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
            $('#categoryName').val('');
            $('#categoryColor').val('#000000');
            $('#colorPicker').css('background-color', '#000000');

            $('#addCategoryModalLabel').text('Adicionar Categoria');
            $('#saveCategoryBtn')
                .text('Salvar Categoria')
                .data('action', 'add')
                .removeData('id');

            $('#addCategoryModal').modal('show');
        });
    },

    handleEditCategoryModal: function () {
        $('.edit-category-btn').click(function () {
            const id = $(this).data('id');
            const nome = $(this).data('nome');
            const cor = $(this).data('cor');

            $('#categoryName').val(nome);
            $('#categoryColor').val(cor);
            $('#colorPicker').css('background-color', cor);

            $('#addCategoryModalLabel').text('Editar Categoria');
            $('#saveCategoryBtn')
                .text('Salvar Alterações')
                .data('action', 'edit')
                .data('id', id);

            $('#addCategoryModal').modal('show');
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