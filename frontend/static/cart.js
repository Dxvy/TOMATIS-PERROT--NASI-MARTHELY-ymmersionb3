function add_to_cart() {
    // get cart from local storage
    // check if object is already in cart
    // if yes, increase amount
    // if no, add object to cart
    // save cart to local storage
    // update cart number in html
}

function removeFromCart() {
    // amount -= 1
    // if amount == 0, remove object from cart
    // save cart to local storage
    // update cart number in html
}

function addFromCart() {
    // amount += 1
    // save cart to local storage
    // update cart number in html
}

function deleteInCart() {
    // remove object from cart
    // save cart to local storage
    // update cart number in html
}

function getCart() {
    // get cart from local storage
    // return cart
}

function saveCart() {
    // save cart to local storage
}

function updateCartNumber() {
    // get cart from local storage
    // get cart length
    // update cart number in html
}

function getTotalItemsPrice() {
    // get cart from local storage
    // multiply item amount with item price
    // return item total price
}

function getTotalPrice() {
    let cart = window.localStorage.getItem('cart');
    let cartParsed = JSON.parse(cart);
    let totalPrice = 0;
    for (let i = 0; i < cartParsed.length; i++) {
        totalPrice += cartParsed[i].price;
    }
    return totalPrice;
}

window.onload = function() {
    if (localStorage.getItem("cart") === null) {
        window.localStorage.setItem("cart", JSON.stringify([]));
    }

    let cart = window.localStorage.getItem('cart');
    let cartParsed = JSON.parse(cart);
    let cartAmount = cartParsed.length;

    if (cartAmount > 0) {
        // create each cart item

    } else {
        // display empty cart message
    }

    // display total price, for each item in cart, add price to total

}