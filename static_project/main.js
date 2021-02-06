$(document).ready(function() {
    $('.update_account').click(function() {
        $('.ui.modal.update').modal('show');
    })

    $('#friend_list_popup').click(function() {
        $('.ui.modal.friendlist').modal('show');
    })

    $('.login_modal').click(function() {
        $('.ui.modal.login').modal('show');
    })

    $('.ui.dropdown')
        .dropdown();
})