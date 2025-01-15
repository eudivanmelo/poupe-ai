
var Alerts = (function () {
    var init_buttons = function () {
        $('[id^="detail-help-"]').click(function (e) {
            var itemId = $(this).data('item-id')
            var modal = $('#detailModal')

            modal.modal('show')
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