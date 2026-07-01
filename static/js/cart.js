// =========================================
// DOURADOS
// CART.JS
// =========================================

// Carrinho guardado no navegador
let cart = JSON.parse(localStorage.getItem("cart")) || [];

// =========================================
// GUARDAR
// =========================================
function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

}

// =========================================
// ADICIONAR
// =========================================
function addToCart(id, nome, preco) {

    preco = Number(preco);

    let item = cart.find(p => p.id == id);

    if (item) {

        item.quantidade++;

    } else {

        cart.push({

            id: id,
            nome: nome,
            preco: preco,
            quantidade: 1

        });

    }

    saveCart();

updateHiddenField();

updateFloatingCart();

}

// =========================================
// REMOVER
// =========================================
function removeItem(id) {

    cart = cart.filter(p => p.id != id);

    saveCart();

    renderCart();

}

// =========================================
// +
// =========================================
function increase(id) {

    let item = cart.find(p => p.id == id);

    if (!item) return;

    item.quantidade++;

    saveCart();

    renderCart();

}

// =========================================
// -
// =========================================
function decrease(id) {

    let item = cart.find(p => p.id == id);

    if (!item) return;

    item.quantidade--;

    if (item.quantidade <= 0) {

        removeItem(id);

        return;

    }

    saveCart();

    renderCart();

}

// =========================================
// TOTAL
// =========================================
function totalCart() {

    let total = 0;

    cart.forEach(item => {

        total += item.preco * item.quantidade;

    });

    return total;

}

// =========================================
// RENDER
// =========================================
function renderCart() {

    let lista = document.getElementById("cart-items");

    if (!lista) return;

    lista.innerHTML = "";

    if (cart.length == 0) {

        lista.innerHTML =
        "<p>🛒 Carrinho vazio.</p>";

        let total = document.getElementById("cart-total");

        if(total){

            total.innerHTML = "0 MT";

        }

        updateHiddenField();

        return;

    }

    cart.forEach(item => {

        lista.innerHTML += `

        <div class="cart-item">

            <div>

                <strong>${item.nome}</strong>

                <br>

                ${item.preco} MT

            </div>

            <div>

                <button onclick="decrease('${item.id}')">-</button>

                ${item.quantidade}

                <button onclick="increase('${item.id}')">+</button>

                <button onclick="removeItem('${item.id}')">

                    🗑

                </button>

            </div>

        </div>

        `;

    });

    let total = document.getElementById("cart-total");

    if(total){

        total.innerHTML = totalCart() + " MT";

    }

    updateHiddenField();

}

// =========================================
// HIDDEN FIELD
// =========================================
function updateHiddenField() {

    let campo = document.getElementById("pedido-hidden");

    if (!campo) return;

    campo.value = JSON.stringify(cart);

}

// =========================================
// CONTADOR
// =========================================
function cartCount() {

    return cart.reduce(

        (a,b)=>a+b.quantidade,

        0

    );

}

// =========================================
// INICIAR
// =========================================
document.addEventListener(

    "DOMContentLoaded",

    function(){

        renderCart();

    }

);

function updateFloatingCart(){

    let badge = document.getElementById("cart-counter");

    if(!badge) return;

    badge.innerHTML = cartCount();

}
