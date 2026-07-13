// =====================================================
// DOURADOS - APP.JS (GLOBAL)
// =====================================================

// ================================
// ACESSO ADMIN DISCRETO
// Toque/clique 5x rápido no logo abre o login admin.
// (Além do ícone de engrenagem já visível.)
// ================================
document.addEventListener("DOMContentLoaded", function () {

    const trigger = document.getElementById("admin-trigger");
    if (!trigger) return;

    let clicks = 0;
    let timer = null;

    trigger.addEventListener("click", function () {

        clicks++;

        clearTimeout(timer);
        timer = setTimeout(function () {
            clicks = 0;
        }, 1200);

        if (clicks >= 5) {
            clicks = 0;
            window.location.href = "/admin/login";
        }
    });
});
