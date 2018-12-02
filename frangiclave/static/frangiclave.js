$(function() {
    $('.section-title').click(function () {
        $(this).next('.section-list').slideToggle();
    });

    $('#action-load').click(function () {
        $.get('/load/');
    });

    var activeSectionItem = document.getElementById('section-item-active');
    if (activeSectionItem != null) {
        activeSectionItem.scrollIntoView();
        window.scrollTo(0, 0);
    }
});
