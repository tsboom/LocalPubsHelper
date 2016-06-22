jQuery(document).ready(function($){
    
    //show spinner by removing bootstrap css class
    $('.load').click(function(e) {
        $('.spinner').removeClass('hidden');

        // while(true){
        //     $.get('/log', function(response){
        //         $('.logbox').text(response.data.logText);
        //     });
        //     setTimeout(3000);
        // }

    });



});