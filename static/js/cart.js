let cart = JSON.parse(localStorage.getItem("cart")) || [];

// ==========================================
// ADICIONAR ITEM AO CARRINHO
// ==========================================
function addToCart(name, price) {

    let existing = cart.find(item => item.name === name);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({
            name: name,
            price: price,
            qty: 1
        });
    }

    saveCart();

    // animação simples de feedback
    showToast("Adicionado ao carrinho 🛒");
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
