


function myFunction() {
    swal("Hello world!");
    console.log("haiffdfdf")
    // code here CAN use carName
}

$(document).ready(function () {

    

    $(function () {
        $('.changeQuantity').submit(function (event) {
            event.preventDefault();
            var product_id = $(this).closest('product_data').find('.prod_id').val();
            var product_qty = $(this).closest('product_data').find('.qty-input').val();
            var product_id = $('.prod_id').val();
            //var product_qty = $('.qty-input').val();
            //var token = $('input[name=csrfmiddlewaretoken]').val();
            //  var cid = $('#ctid').val();
            //var pid = $('#ctptid').val();

            $.ajax({
                method: "POST",
                url: "cart/updatecart",
                data: {
                    'product_id': product_id,
                    'product_qty': product_qty,
                    csrfmiddlewaretoken: token,

                },


                success: function (response) {
                    // Update the shopping cart display
                    //$('#cart-count').text(response.cart_count);
                    //$('#cart-total').text(response.cart_total);
                    swal(response.status)
                    // Show a success message
                    alert('Item added to cart!');
                },
                error: function (response) {
                    // Show an error message
                    alert('An error occurred while adding the item to the cart.');
                }
            });
        });
    });

});

