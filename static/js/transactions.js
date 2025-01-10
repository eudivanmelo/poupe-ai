const EditTransaction = (itemId) => {
    // $('#recipient-name').val('Recipient ' + itemId);
    // $('#message-text').val('Message content for transaction ' + itemId);

    $('#editModal').modal('show');
}

var Alerts = (function () {
    var init_buttons = function () {
        $('[id^="detail-transaction-"]').click(function (e) {
            var itemId = $(this).data('item-id')
            var modal = $('#detailModal')

            modal.find('#modal-edit-button').click(() => {
                modal.modal('hide')
                EditTransaction(itemId)
            })
            
            modal.modal('show')
        })

        $('[id^="edit-transaction-"]').click(function (e) {
            var itemId = $(this).data('item-id')

            EditTransaction(itemId)
        })

        $('[id^="delete-transaction-"]').click(function (e) {
            var itemId = $(this).data('item-id')

            swal({
                title: 'Tem certeza?',
                text: `Ao apagar a transação (${itemId}) você não poderá reverter isso!`,
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
                        text: 'A transação foi removida com sucesso.',
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
    Alerts.init()
})