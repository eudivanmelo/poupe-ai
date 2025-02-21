const EditAccount = (itemId) => {
    // $('#recipient-name').val('Recipient ' + itemId);
    // $('#message-text').val('Message content for transaction ' + itemId);

    $('#editModal').modal('show');
}

var Modals = (function () {
    var init_buttons = function () {
        $('[id^="detail-account-"]').click(function (e) {
            var itemId = $(this).data('item-id')
            var modal = $('#detailModal')

            modal.find('#modal-edit-button').click(() => {
                modal.modal('hide')
                EditAccount(itemId)
            })
            
            modal.modal('show')
        })

        $('[id^="edit-account-"]').click(function (e) {
            var itemId = $(this).data('item-id')

            EditAccount(itemId)
        })

        $('[id^="delete-account-"]').click(function (e) {
            var itemId = $(this).data('item-id')

            swal({
                title: 'Tem certeza?',
                text: `Ao apagar a conta (${itemId}) todas as transações vinculadas a ela também serão apagadas, este processo não pode ser revertido!`,
                type: 'warning',
                buttons: {
                    confirm: {
                        text: 'Sim, deletar!',
                        className: 'btn btn-secondary'
                    },
                    cancel: {
                        visible: true,
                        className: 'btn btn-danger'
                    }
                }
            }).then((Delete) => {
                if (Delete) {
                    swal({
                        title: 'Deletado!',
                        text: 'A conta foi removida com sucesso.',
                        type: 'success',
                        buttons: {
                            confirm: {
                                className: 'btn btn-success'
                            }
                        }
                    })
                } else {
                    swal.close()
                }
            })
        })
    }

    return {
        init: function () {
            init_buttons()
        }
    }
})()

jQuery(document).ready(function () {
    Modals.init()
})