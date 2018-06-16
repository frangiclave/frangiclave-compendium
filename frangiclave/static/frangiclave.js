$(function() {
    $('.section-title').click(function () {
        $(this).next('.section-list').slideToggle();
    });

    $('#action-load').click(function () {
        $.get('/load/');
    })
});
