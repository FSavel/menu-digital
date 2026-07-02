let cart = JSON.parse(localStorage.getItem("cart")) || [];

// ==========================================
// ADICIONAR ITEM AO CARRINHO
// ==========================================
function addToCart(name, price) {

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    let existing = cart.find(item => item.name === name);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ name, price, qty: 1 });
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    renderCart();
    updateCartCounter();
    showToast("Adicionado 🛒");
}

// ==========================================
// REMOVER / ALTERAR
// ==========================================
function changeQty(index, value) {
    cart[index].qty += value;

    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }

    saveCart();
}

function removeItem(index) {
    cart.splice(index, 1);
    saveCart();
}

// ==========================================
// GUARDAR
// ==========================================
function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCounter();
    renderCart();
}

// ==========================================
// CONTADOR FLUTUANTE
// ==========================================
function updateCartCounter() {

    let totalItems = 0;

    cart.forEach(item => {
        totalItems += item.qty;
    });

    const counter = document.getElementById("cart-counter");

    if (counter) {
        counter.innerText = totalItems;
    }
}

// ==========================================
// TOAST (FEEDBACK VISUAL)
// ==========================================
function showToast(message) {

    let toast = document.createElement("div");

    toast.innerText = message;

    toast.style.position = "fixed";
    toast.style.bottom = "80px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.background = "#27ae60";
    toast.style.color = "white";
    toast.style.padding = "10px 15px";
    toast.style.borderRadius = "8px";
    toast.style.zIndex = "9999";
    toast.style.fontSize = "14px";

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 1500);
}

// ==========================================
// INIT
// ==========================================
updateCartCounter();

function renderCart() {

    const container = document.getElementById("cart-items");
    const totalEl = document.getElementById("cart-total");

    if (!container || !totalEl) return;

    container.innerHTML = "";

    let total = 0;

    if (cart.length === 0) {
        container.innerHTML = "<p>Nenhum item ainda</p>";
        totalEl.innerText = "0";
        return;
    }

    cart.forEach((item, index) => {

        total += item.price * item.qty;

        const div = document.createElement("div");
        div.className = "item";

        div.innerHTML = `
            <div>
                <strong>${item.name}</strong><br>
                <small>${item.qty} x ${item.price}</small>
            </div>

            <div>
                <button onclick="changeQty(${index}, 1)">+</button>
                <button onclick="changeQty(${index}, -1)">-</button>
                <button onclick="removeItem(${index})">🗑</button>
            </div>
        `;

        container.appendChild(div);
    });

    totalEl.innerText = total.toFixed(2);
}

renderCart();
updateCartCounter();

function checkout() {

    if (cart.length === 0) {
        showToast("Carrinho vazio!");
        return;
    }

    fetch("/pedido", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cart: cart
        })
    })
    .then(res => res.json())
    .then(data => {

        if (data.success) {

            showToast("Pedido enviado com sucesso 🍽️");

            cart = [];

            saveCart();

            renderCart();

        } else {
            showToast("Erro ao enviar pedido");
        }

    })
    .catch(err => {
        console.error(err);
        showToast("Erro de ligação ao servidor");
    });
}

function updateCartUI() {

    const counter = document.getElementById("cart-counter");

    if (!counter) return;

    let totalItems = 0;

    cart.forEach(item => {
        totalItems += item.qty;
    });

    counter.innerText = totalItems;

    // efeito visual "crescer carrinho"
    if (totalItems > 0) {
        counter.style.transform = "scale(1.3)";
        setTimeout(() => {
            counter.style.transform = "scale(1)";
        }, 200);
    }
}

function renderCart() {

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    let container = document.getElementById("cart-items");
    let totalEl = document.getElementById("cart-total");

    if (!container) return;

    container.innerHTML = "";

    let total = 0;

    cart.forEach((item, index) => {

        total += item.price * item.qty;

        container.innerHTML += `
        <div class="item">
            <span>${item.name} x${item.qty}</span>
            <span>${item.price * item.qty} MT</span>
        </div>`;
    });

    totalEl.innerText = total + " MT";
}
renderCart();
function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

function syncCartUI() {

    let cart = getCart();

    let totalItems = 0;

    cart.forEach(item => {
        totalItems += item.qty;
    });

    const counter = document.getElementById("cart-counter");

    if (counter) {
        counter.innerText = totalItems;
    }
}
