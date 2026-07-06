// =====================================================
// DOURADOS - CART.JS
// Versão 2.0
// =====================================================

// ================================
// CARRINHO
// ================================
let cart = JSON.parse(localStorage.getItem("cart")) || [];

// ================================
// GUARDAR
// ================================
function saveCart() {

    localStorage.setItem("cart", JSON.stringify(cart));

    updateCartCounter();

    renderCart();
}

// ================================
// ADICIONAR PRODUTO
// ================================
function addToCart(name, price) {

    price = Number(price);

    const existing = cart.find(item => item.name === name);

    if (existing) {
        existing.qty++;
    } else {

        cart.push({
            name: name,
            price: price,
            qty: 1
        });

    }

    saveCart();

    animateCart();

    showToast("🛒 Produto adicionado");
}

// ================================
// ALTERAR QUANTIDADE
// ================================
function changeQty(index, value) {

    if (!cart[index]) return;

    cart[index].qty += value;

    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }

    saveCart();
}

// ================================
// REMOVER ITEM
// ================================
function removeItem(index) {

    cart.splice(index, 1);

    saveCart();
}

// ================================
// LIMPAR CARRINHO
// ================================
function clearCart() {

    cart = [];

    saveCart();
}

// ================================
// CONTADOR
// ================================
function updateCartCounter() {

    const counter = document.getElementById("cart-counter");

    if (!counter) return;

    let total = 0;

    cart.forEach(item => {

        total += item.qty;

    });

    counter.innerText = total;

    counter.style.display = total > 0 ? "flex" : "none";
}

// ================================
// ANIMAÇÃO DO CARRINHO
// ================================
function animateCart() {

    const counter = document.getElementById("cart-counter");

    if (!counter) return;

    counter.style.transform = "scale(1.35)";

    setTimeout(() => {

        counter.style.transform = "scale(1)";

    },200);

}

// ================================
// TOAST
// ================================
function showToast(message) {

    const toast = document.createElement("div");

    toast.innerText = message;

    toast.style.position = "fixed";
    toast.style.bottom = "80px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.background = "#27ae60";
    toast.style.color = "white";
    toast.style.padding = "12px 18px";
    toast.style.borderRadius = "10px";
    toast.style.fontSize = "14px";
    toast.style.zIndex = "9999";
    toast.style.boxShadow = "0 6px 20px rgba(0,0,0,.3)";

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.remove();

    },1500);

}

// ================================
// RENDER CARRINHO
// ================================
function renderCart() {

    const container = document.getElementById("cart-items");

    if (!container) return;

    const totalEl =
        document.getElementById("cart-total") ||
        document.getElementById("total");

    container.innerHTML = "";

    if (cart.length === 0) {

        container.innerHTML =
            "<p class='empty'>Carrinho vazio</p>";

        if (totalEl)
            totalEl.innerText = "0 MT";

        return;
    }

    let total = 0;

    cart.forEach((item,index)=>{

        total += item.price * item.qty;

        container.innerHTML += `

        <div class="item">

            <div class="item-name">

                <strong>${item.name}</strong>

            </div>

            <div class="qty">

                <button onclick="changeQty(${index},-1)">−</button>

                ${item.qty}

                <button onclick="changeQty(${index},1)">+</button>

            </div>

            <div class="item-price">

                ${(item.price*item.qty).toFixed(2)} MT

            </div>

            <button class="remove"
                    onclick="removeItem(${index})">

                ✕

            </button>

        </div>

        `;

    });

    if(totalEl){

        totalEl.innerText = total.toFixed(2)+" MT";

    }

    const pedidoData=document.getElementById("pedido-data");

    if(pedidoData){

        pedidoData.value=JSON.stringify(cart);

    }

}

// ================================
// CHECKOUT
// ================================
function checkout() {

    if(cart.length===0){

        showToast("Carrinho vazio");

        return;

    }

    fetch("/pedido",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            cart:cart
        })

    })

    .then(r=>r.json())

    .then(data=>{

        if(data.success){

            showToast("Pedido enviado 🍽️");

            clearCart();

        }

        else{

            showToast("Erro ao enviar");

        }

    })

    .catch(err=>{

        console.error(err);

        showToast("Erro de ligação");

    });

}

// ================================
// SINCRONIZAR ENTRE PÁGINAS
// ================================
window.addEventListener("storage",function(){

    cart = JSON.parse(localStorage.getItem("cart")) || [];

    updateCartCounter();

    renderCart();

});

// ================================
// INICIALIZAÇÃO
// ================================
document.addEventListener("DOMContentLoaded",function(){

    cart = JSON.parse(localStorage.getItem("cart")) || [];

    updateCartCounter();

    renderCart();

});
