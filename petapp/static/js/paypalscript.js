<script>    

        var amount = {{ totalbill }};
        function initPayPalButton() {
            document.getElementById("paypapl").style.visibility = "hidden";
            paypal.Buttons({
                style: {
                    shape: 'rect',
                    color: 'gold',
                    layout: 'vertical',
                    label: 'paypal',
                },
                createOrder: function (data, actions) {
                    return actions.order.create({
                        purchase_units: [{ "amount": { "currency_code": "USD", "value": amount } }]
                    });
                },
                onApprove: function (data, actions) {
                    return actions.order.capture().then(function (orderData) {
                        console.log(orderData);
                        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                        var data = orderData['id'];
                        var odata = {{ orderobj.ordernumber }};
                        window.location.replace("paymentsucess/" + data + "/" + odata + "/");
                    });
                },
                onError: function (err) {
                    console.log(err);
                }
            }).render('#paypal-button-container');
        }
    </script>
