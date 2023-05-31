$(function () { 
    $('#accordion li span').click(function() { 
        $(this).next('ul').slideToggle(); 
    }); 
});