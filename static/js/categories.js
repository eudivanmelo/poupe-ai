$(document).ready(function () {
    // Adicionar evento de click para os botões de excluir categoria
    $('[id^="delete-category-"]').click(function () {
        const itemId = $(this).data('id');
        const itemName = $(this).data('nome');

        // Exibe o modal de confirmação usando SweetAlert
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
                // Realiza a exclusão
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
                    // Atualização no front-end
                    $(`#category-${itemId}`).remove();
                    console.log(`Categoria "${itemName}" movida para "Outros"`);
                });
            } else {
                swal.close();
            }
        });
    });

    // Atualizar a cor do círculo ao selecionar a cor
    $('#categoryColor').on('input', function () {
        const color = $(this).val();
        $('#colorPicker').css('background-color', color);
    });

    // Abrir seletor de cor ao clicar no círculo
    $('#colorPicker').click(function () {
        $('#categoryColor').click();
    });

    // Alternar entre abas e atualizar os valores totais
    $('#categoryTabs .nav-link').on('shown.bs.tab', function (event) {
        const newTotal = $(event.target).data('total');
        const newCatTotal = $(event.target).data('total-cat');
        $('#total-value').text(`R$ ${newTotal}`);
        $('#total-categorias').text(`${newCatTotal}`);
    });

    // Abrir o modal para adicionar categoria
    $('#add-category').click(function () {
        $('#categoryName').val('');
        $('#categoryColor').val('#000000');
        $('#colorPicker').css('background-color', '#000000');

        $('#addCategoryModalLabel').text('Adicionar Categoria');
        const saveButton = $('#saveCategoryBtn');
        saveButton.text('Salvar Categoria').data('action', 'add').removeData('id');

        $('#addCategoryModal').modal('show');
    });

    // Abrir o modal para editar categoria
    $('.edit-category-btn').click(function () {
        const id = $(this).data('id');
        const nome = $(this).data('nome');
        const cor = $(this).data('cor');

        $('#categoryName').val(nome);
        $('#categoryColor').val(cor);
        $('#colorPicker').css('background-color', cor);

        $('#addCategoryModalLabel').text('Editar Categoria');
        const saveButton = $('#saveCategoryBtn');
        saveButton.text('Salvar Alterações').data('action', 'edit').data('id', id);

        $('#addCategoryModal').modal('show');
    });

    // Impressão do tipo da categoria ao alternar entre abas
    $('#categoryTabs .nav-link').on('shown.bs.tab', function (event) {
        console.log('Categoria selecionada:', $(event.target).text());
    });
});