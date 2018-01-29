jQuery(document).ready(function($) {

    //show spinner by removing bootstrap css class
    $('#load').click(function(e) {
        $('.loading-dots').show();

    });

    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');


});
