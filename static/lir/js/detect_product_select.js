$(document).on('change','#product_name',function(){
    location.href = '/lir/report/' + $( "#product_name option:selected" ).text() + '/';
});