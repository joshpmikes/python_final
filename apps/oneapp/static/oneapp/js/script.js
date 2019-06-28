$(document).ready(function(){

    $('#all_categories').hide();


    $('#show').click(function(){
        $('#all_categories').show();
        console.log("hello")
    })

    $('#modal1').modal();
    $('select').formSelect();

})