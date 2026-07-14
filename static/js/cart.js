// =====================================================
// DOURADOS - CART.JS (VERSÃO LIMPA FINAL)
// =====================================================

// ================================
// ESTADO GLOBAL DO CARRINHO
// ================================
let cart = getCart();

// ================================
// OBTÉM CARRINHO DO LOCALSTORAGE
// ================================
function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

// ================================
// SALVAR CARRINHO
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

    cart = getCart(); // garante sincronização

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
// CONTADOR FLUTUANTE
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
    }, 200);
}

// ================================
// TOAST (FEEDBACK VISUAL)
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

    setTimeout(() => toast.remove(), 1500);
}

// ================================
// RENDER DO CARRINHO (PÁGINA CART)
// ================================
function renderCart() {

    const container = document.getElementById("cart-items");
    if (!container) return;

    const totalEl =
        document.getElementById("cart-total") ||
        document.getElementById("total");

    container.innerHTML = "";

    if (cart.length === 0) {
        container.innerHTML = "<p class='empty'>Carrinho vazio</p>";

        if (totalEl) totalEl.innerText = "0 MT";
        return;
    }

    let total = 0;

    cart.forEach((item, index) => {

        const itemTotal = item.price * item.qty;
        total += itemTotal;

        container.innerHTML += `
            <div class="item">

                <div class="item-name">
                    <strong>${item.name}</strong>
                </div>

                <div class="qty">
                    <button onclick="changeQty(${index}, -1)">-</button>
                    ${item.qty}
                    <button onclick="changeQty(${index}, 1)">+</button>
                </div>

                <div class="item-price">
                    ${itemTotal.toFixed(2)} MT
                </div>

                <button class="remove" onclick="removeItem(${index})">
                    ✕
                </button>

            </div>
        `;
    });

    if (totalEl) {
        totalEl.innerText = total.toFixed(2) + " MT";
    }

    const pedidoData = document.getElementById("pedido-data");
    if (pedidoData) {
        pedidoData.value = JSON.stringify(cart);
    }
}

// ================================
// CHECKOUT (ATUALIZADO PARA GOOGLE SHEETS)
// ================================
function checkout() {
    cart = getCart();
    
    // Recupera o nome que o cliente digitou no menu
    const nomeCliente = localStorage.getItem("nome_cliente") || "Cliente";

    if (cart.length === 0) {
        showToast("Carrinho vazio");
        return;
    }

    // Junta todos os produtos numa linha de texto limpa. Ex: "2x Pizza, 1x Coca-cola"
    const produtosTexto = cart.map(item => `${item.qty}x ${item.name}`).join(", ");

    // Calcula o valor total do carrinho
    let totalPreco = 0;
    cart.forEach(item => {
        totalPreco += item.price * item.qty;
    });

    // Cria exatamente o formato que o teu Google Sheets espera receber!
    const pacoteDados = {
        id: "PED-" + Date.now().toString().slice(-5), // Cria um ID curto como PED-48291
        nome: nomeCliente,
        pedido: produtosTexto,
        total: totalPreco.toFixed(2),
        hora: new Date().toLocaleTimeString("pt-PT", { hour: '2-digit', minute: '2-digit' }),
        status: "Recebido"
    };

    fetch("/pedido", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pacoteDados) // Envia o pedido arrumadinho
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast("Pedido enviado 🍽️");
            clearCart();
            localStorage.removeItem("nome_cliente"); // Apaga o nome para o próximo pedido
            
            // Espera 2 segundos e volta ao menu principal
            setTimeout(() => {
                window.location.href = "/";
            }, 2000);
        } else {
            showToast("Erro ao enviar");
        }
    })
    .catch(err => {
        console.error(err);
        showToast("Erro de ligação");
    });
}

// ================================
// SINCRONIZAÇÃO ENTRE PÁGINAS
// ================================
window.addEventListener("storage", () => {
    cart = getCart();
    updateCartCounter();
    renderCart();
});

// ================================
// INICIALIZAÇÃO
// ================================
document.addEventListener("DOMContentLoaded", () => {
    cart = getCart();
    updateCartCounter();
    renderCart();
});
