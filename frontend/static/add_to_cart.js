function add_to_cart(product) {
    let cart = JSON.parse(window.localStorage.getItem('cart')) || {};
    let found = false;

    for (let key in cart) {
        if (cart[key].id === product) {
            cart[key].amount += 1;
            found = true;
            break;
        }
    }

    if (!found) {
        let cart_length = Object.keys(cart).length;
        cart[cart_length] = {
            id: product,
            amount: 1
        };
    }
    console.log(cart);

    window.localStorage.setItem("cart", JSON.stringify(cart));
}
