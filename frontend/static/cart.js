function decreaseItemInCart() {
    // amount -= 1
    // if amount == 0, remove object from cart
    // save cart to local storage
    // update cart number in html

    updateCartLength();
}

function increaseItemInCart() {
    // amount += 1
    // save cart to local storage
    // update cart number in html

    updateCartLength();
}

function deleteItemInCart(clicked_id) {
    document.getElementById(clicked_id).remove();
    // remove item from local storage
    // let cart = getCart();
    // delete cart[clicked_id];
    window.localStorage.setItem("cart", JSON.stringify(cart));
    if (document.querySelectorAll(".item").length === 0) {
        let buyPhase = document.querySelector(".buy-phase");
        buyPhase.innerHTML = "Your cart is empty";
    }

    updateCartLength();
}

function getCart() {
    return JSON.parse(window.localStorage.getItem('cart')) || {};
}

function saveCart() {
    // save cart to local storage
}

function updateCartLength() {
    let cart = getCart();
    let cartLength = 0;
    // need to add the amount of each item in cart
    for (let key in cart) {
        // add amount of each item in cart
        cartLength += cart[key].amount;
    }
    // update cart number in html
    document.getElementById("cart-length").innerHTML = cartLength.toString();
}

function getTotalItemsPrice() {
    // get cart from local storage
    // multiply item amount with item price
    // return item total price
}

function getItemFromId(id) {
    // get all info from db

    // return item

    // return null if item not found


}

function add_to_cart(product) {
    let cart = getCart();
    let found = false;

    for (let key in cart) {
        if (cart[key].id === product) {
            cart[key].amount += 1;
            found = true;
            break;
        }
    }

    if (!found) {
        let cartLength = Object.keys(cart).length;
        cart[cartLength] = {
            id: product,
            amount: 1
        };
    }
    console.log(cart);

    window.localStorage.setItem("cart", JSON.stringify(cart));

    updateCartLength();
}

function createItemsInCart() {
    let cart = window.localStorage.getItem('cart');
    console.log(cart);
    let cartParsed = JSON.parse(cart);
    let cartAmount = cartParsed.length;

    let buyPhase = document.querySelector('.buy-phase');

    function appendItemToDOM(item, cartAmount) {
        buyPhase.innerHTML += `
            <div class="item" id="${item['id']}">
                <div class="item-content">
                    <div class="item-image-div">
                        <img class="item-image" src="/static/images/${item['id']}-1.jpeg" alt="">
                    </div>
                    <div class="item-description">
                        <div class="item-price-infos">
                            <p class="item-price">${item['price']} €</p>
                        </div>
                        <p class="item-name">${item.name}</p>
                    </div>
                </div>
                <div class="item-management">
                    <div class="add-more-number hide">
                        <div class="add-more">
                            <i class="fa-solid fa-plus"></i>
                        </div>
                        <div class="add-less">
                            <i class="fa-solid fa-minus"></i>
                        </div>
                        <div class="more-number">${cartAmount}</div>
                    </div>
                    <div class="delete-item" onclick="deleteItemInCart(${item['id']})">Delete</div>
                </div>
            </div>
        `;
    }

    let fetchPromises = [];

    for (let i = 0; i < cartAmount; i++) {
        fetchPromises.push(
            searchDatabase(cartParsed[i].id)
                .then(data => {
                    appendItemToDOM(data, cartParsed[i].amount);
                })
                .catch(error => {
                    console.error('Error:', error);
                })
        );
    }

    Promise.all(fetchPromises)
        .then(() => {
            console.log('All items fetched and added to the DOM.');
        })
        .catch(error => {
            console.error('Error fetching items:', error);
        });
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


function searchDatabase(itemId) {
    return new Promise((resolve, reject) => {
        fetch(`/api/get_row/${itemId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Row from database:', data);
                resolve(data);
            })
            .catch(error => {
                console.error('Error:', error);
                reject(error);
            });
    });
}

window.onload = function() {
    updateCartLength();

    if (localStorage.getItem("cart") === null) {
        window.localStorage.setItem("cart", JSON.stringify([]));
    }

    let cart = window.localStorage.getItem('cart');
    let cartParsed = JSON.parse(cart);
    let cartAmount = cartParsed.length;

    let fileName = location.href.split("/").slice(-1);

    if (String(fileName) === "cart")
    {
        console.log("cart");
        if (cartAmount === 0) {
            console.log("empty");
            let buyPhase = document.querySelector(".buy-phase");
            buyPhase.innerHTML = "Your cart is empty";
        } else {
            createItemsInCart();
        }
    } else {
        console.log("not cart");
    }

    // display total price, for each item in cart, add price to total

}