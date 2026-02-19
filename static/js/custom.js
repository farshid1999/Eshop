function scroll_text(){
       document.getElementById("commentinfo").scrollIntoView({behavior:"smooth"})
}



function filter_price(){
       const filter_prices = $('#sl2').val()
       const start_price = filter_prices.split(',')[0]
       const end_price = filter_prices.split(',')[1]

       $('#start_price').val(start_price)
       $('#end_price').val(end_price)
       $('#filter_form').submit()

}

function increase() {
            var current_val = parseInt($("#count-product-to-buy").val()); // Get current value as integer
            $("#count-product-to-buy").val(current_val + 1); // Increment value
        }

 function decrease() {
            var current_val = parseInt($("#count-product-to-buy").val()); // Get current value as integer
            if (current_val > 0) { // Prevent going below 0
                $("#count-product-to-buy").val(current_val - 1); // Decrement value
            }
        }



function change_photo(event,curent){
    event.preventDefault()
    temp=$("#legend-picture").attr("src")
    $("#legend-picture").attr("src", $("#" + curent).attr("src"));
    $("#" + curent).attr("src", temp);
}


$(document).on("submit", "#comment-form", function (event) {
    event.preventDefault();
    var comment = $("#comment-prod").val();
    var prodid = $("#prod-id").val();
    var userid = $("#user-id").val();

    $.ajax({
        url: $("#comment-form").attr("action"),
        type: "POST",
        data: {
            "comment-text-name": comment,
            "product-id-name": prodid,
            "user-id-name": userid,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            $("#http-response")
                .html(response)
                .removeClass('alert-danger')
                .addClass('alert-success')
                .show();
            $('#comment-prod').val('');
        },
        error: function () {
            $("#http-response")
                .html("خطا در ارسال دیدگاه!")
                .removeClass('alert-success')
                .addClass('alert-danger')
                .show();
        }
    });
});

function add_order_product(productid){
    count=$("#count-product-to-buy").val()
    $.get('/order/add-to-order?product_id=' + productid + '&count=' + count).then(res=>{
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon, // انواع آیکن: success, error, warning, info, question
            width:'40vw',
            height:'600px',
            confirmButtonText: 'باشه'
        }).then(result=>{
            if(res.status==="not_auth" && result.isConfirmed){
                location.href='/login';
            }
        })

    })
}

function remove_product(product_id,event){
    event.preventDefault()
    $.get('/order/delete-product-order?product_id=' + product_id).then(res=>{
        if (res.status==='delete_succese'){
            console.log(res)
            reset_sum_price(product_id)
            $('#order-'+product_id).remove()

        }
        if (res.status==='product_id_invalid'){
            console.log(res)
        }
        if (res.status==='product_not_found'){
            console.log(res)
        }
    })
}

function reset_sum_price(product_id) {
    var count = parseInt($("#count-" + product_id).val())
    var del_val = parseFloat($("#price-" + product_id).attr("data-value") * count);
    var sum_val = parseFloat($("#sum-orders").attr("data-value"));
    var newval = sum_val - del_val;
    $("#sum-orders").attr("data-value", newval);
    $("#sum-orders").html(newval.toLocaleString('fa-IR') + " تومان");
}

function set_discount_order(userid,event){
    event.preventDefault()
    const code=$('#discount_code').val()
    $.get('/order/discount-order?code=' + code + '&userid=' + userid ).then(res=>{
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon, // انواع آیکن: success, error, warning, info, question
            width: '40vw',
            height: '600px',
            confirmButtonText: 'باشه'
        }).then(result=>{
            if(res.status==='succese'){
                var newval = res.final_price
                $("#sum-orders").attr("data-value", newval);
                $("#sum-orders").html(newval.toLocaleString('fa-IR') + " تومان");

            }
        })
    })
}








// function inc_prod(productid,event){
//     event.preventDefault()
//     current_val=parseInt($("#count-"+ productid).val())
//     $("#count-"+ productid).val(current_val+1)
//     count= parseInt($("#count-"+ productid).val())
//     $.get('/order/inc-count-prod?product_id=' +productid + '&count='+count).then(res=>{
//         console.log(res)
//
//     }).catch(err=>{
//         console.log(err)
//     })
// }
// function dec_prod(productid,event){
//     event.preventDefault()
//     if (parseInt($("#count-"+ productid).val())>=2){
//         current_val=parseInt($("#count-"+ productid).val())
//         $("#count-"+ productid).val(current_val-1)
//         count= parseInt($("#count-"+ productid).val())
//         $.get('/order/dec-count-prod?product_id=' +productid + '&count='+count).then(res=>{
//
//     })
//     }
// }
