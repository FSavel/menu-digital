# ======================================================
# IMPORTS
# ======================================================
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import pytz
import os
import json
from flask import jsonify
from functools import wraps
from languages import LANGUAGES
from flask import session

from config import Config

# ======================================================
# HELPERS
# ======================================================
from utils.helpers import (
    hora_mocambique,
    gerar_id,
    moeda
)
def admin_required_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper
# ======================================================
# SERVICES
# ======================================================
from services.order_service import (
    add_order,
    get_orders,
    get_last_orders,
    get_dashboard_stats,
    update_order_status,
    get_order_by_id,
    delete_order,
    get_total_sales
)

app = Flask(__name__)
def get_language(lang):

    if lang not in LANGUAGES:
        lang = "pt"

    return LANGUAGES[lang]

# ======================================================
# MENU SERVICE
# ======================================================
from services.menu_service import (
    load_menu,
    search_menu,
    filter_category,
    get_product
)

# ======================================================
# RESERVATION SERVICE
# ======================================================
from services.reservation_service import (
    add_reservation,
    get_reservations,
    update_reservation_status,
    delete_reservation
)

# ======================================================
# ADMIN SERVICE
# ======================================================
from services.admin_service import (
    dashboard,
    statistics,
    recent_orders
)

# ======================================================
# CALL SERVICE
# ======================================================
from services.call_service import (
    add_call,
    get_calls,
    delete_call,
    total_calls
)

# ======================================================
# KITCHEN SERVICE
# ======================================================
from services.kitchen_service import (
    kitchen_orders,
    kitchen_stats,
    received_orders,
    preparing_orders,
    ready_orders,
    delivered_orders
)

# ======================================================
# TABLE SERVICE
# ======================================================
from services.table_service import (
    get_tables,
    get_table,
    add_table,
    update_table_status,
    assign_customer,
    assign_order,
    free_table,
    table_stats,
    free_tables,
    occupied_tables
)

# ======================================================
# SESSÃO / LOGIN ADMIN
# ======================================================

app.secret_key = "restaurante_secret_key"

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD


# ======================================================
# FUNÇÃO DE PROTEÇÃO (DECORADOR SIMPLES)
# ======================================================
def admin_required():
    return session.get("admin_logged_in") is True


# ======================================================
# LOGIN ADMIN
# ======================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "GET":
        return render_template("admin/login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        flash("Login efetuado com sucesso!", "success")
        return redirect(url_for("pedidos"))

    flash("Credenciais inválidas!", "danger")
    return redirect(url_for("admin_login"))


# ======================================================
# LOGOUT ADMIN
# ======================================================
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)
    flash("Sessão terminada!", "info")
    return redirect(url_for("admin_login"))


# ======================================================
# ATUALIZAR STATUS POR ID (PROFISSIONAL)
# ======================================================
def atualizar_status_por_id(pedido_id, novo_status):
    from services.order_service import update_order_status
    return update_order_status(pedido_id, novo_status)

# ======================================================
# MENU
# ======================================================
def carregar_menu():
    return load_menu()

# ======================================================
# Cart
# ======================================================
@app.route("/cart")
def cart():

    return render_template(
        "cart.html",
        config=Config
    )
# ======================================================
# HOME
# ======================================================
@app.route("/")
def home():
    return render_template(
        "idioma.html",
        config=Config
    )
    
@app.route("/set_language/<lang>")
def set_language(lang):

    if lang not in ["pt", "en"]:
        lang = "pt"

    session["lang"] = lang

    if lang == "en":
        return redirect(url_for("menu_en"))

    return redirect(url_for("menu_pt"))

# ======================================================
# MENU PT & ENG
# ======================================================
@app.route("/menu_pt")
def menu_pt():

    session["lang"]="pt"

    return render_template(
        "menu.html",
        menu=load_menu(),
        lang="pt",
        config=Config
    )


@app.route("/menu_en")
def menu_en():

    session["lang"]="en"

    return render_template(
        "menu.html",
        menu=load_menu(),
        lang="en",
        config=Config
    )

# ======================================================
# CRIAR PEDIDO
# ======================================================
@app.route("/pedido", methods=["POST"])
def pedido():

    data = request.get_json()
    cart = data.get("cart", [])

total = sum(
    item.get("preco", 0) * item.get("quantidade", 1)
    for item in cart
)

    add_order(
        Config.ORDERS_FILE,
        "Cliente",
        cart,
        hora_mocambique()
    )

    return {
        "success": True,
        "total": total
    }


# ======================================================
# CHAMAR GARÇOM
# ======================================================
@app.route("/chamar")
def chamar():

    chamada = {

        "id": gerar_id(),

        "mesa": request.args.get("mesa", "Não informada"),

        "hora": hora_mocambique(),

        "status": "Nova"
    }

    add_call(
        Config.CALLS_FILE,
        chamada
    )

    flash(
        "Garçom chamado com sucesso!",
        "success"
    )

    return redirect(url_for("menu_pt"))


# ======================================================
# DASHBOARD ADMIN
# ======================================================
@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    stats = get_dashboard_stats(Config.ORDERS_FILE)

    pedidos = get_last_orders(
        Config.ORDERS_FILE,
        quantidade=10
    )

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        pedidos=pedidos,
        config=Config
    )

@app.route("/api/cozinha/pedidos")
@admin_required_json
def api_cozinha_pedidos():

    pedidos = get_orders(Config.ORDERS_FILE)

    # ordenar do mais recente para o mais antigo
    pedidos = list(reversed(pedidos))

    return jsonify({
        "success": True,
        "pedidos": pedidos
    })


@app.route("/api/pedido/status", methods=["POST"])
def api_update_status():

    if not session.get("admin_logged_in"):
        return {"error": "unauthorized"}, 401

    data = request.json
    pedido_id = data.get("id")
    novo_status = data.get("status")

    sucesso = update_order_status(
        Config.ORDERS_FILE,
        pedido_id,
        novo_status
    )

    return {
        "success": sucesso,
        "id": pedido_id,
        "status": novo_status
    }

# ======================================================
# MUDAR STATUS POR ID (ADMIN)
# ======================================================
@app.route("/admin/pedido/status/<pedido_id>/<status>")
def mudar_status(pedido_id, status):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    success = update_order_status(
        Config.ORDERS_FILE,
        pedido_id,
        status
    )

    if success:
        flash(f"Status atualizado para {status}", "success")
    else:
        flash("Erro ao atualizar status", "danger")

    return redirect(url_for("cozinha"))

    
# ======================================================
# PAINEL PEDIDOS (COZINHA)
# ======================================================
@app.route("/pedidos")
def pedidos():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pedidos = get_orders(Config.ORDERS_FILE)

    total_dia = get_total_sales(
        Config.ORDERS_FILE
    )

    return render_template(
        "pedidos.html",
        pedidos=pedidos,
        total_dia=total_dia,
        config=Config
    )


# ======================================================
# COZINHA (TEMPO REAL)
# ======================================================
@app.route("/cozinha")
def cozinha():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pedidos = get_orders(Config.ORDERS_FILE)

    # ordenar do mais recente para o mais antigo
    pedidos = list(reversed(pedidos))

    return render_template(
        "cozinha.html",
        pedidos=pedidos,
        config=Config,
        refresh_time=Config.COZINHA_REFRESH
    )


# ======================================================
# MARCAR COMO ENTREGUE
# ======================================================
@app.route("/entregar/<pedido_id>")
def entregar(pedido_id):

    update_order_status(
        Config.ORDERS_FILE,
        pedido_id,
        "Entregue"
    )

    return redirect(url_for("pedidos"))


# ======================================================
# RESERVAS
# ======================================================
@app.route("/reserva", methods=["GET", "POST"])
def reserva():

    if request.method == "GET":
        return render_template(
            "reserva.html",
            config=Config
        )

    novo = {
        "id": gerar_id(),
        "nome": request.form.get("nome"),
        "contacto": request.form.get("contacto"),
        "tipo": request.form.get("tipo", ""),
        "descricao": request.form.get("descricao", ""),
        "quantidade": request.form.get("quantidade", ""),
        "data": request.form.get("data"),
        "observacoes": request.form.get("observacoes", ""),
        "hora": hora_mocambique(),
        "status": "Pendente"
    }

    add_reservation(Config.RESERVATIONS_FILE, novo)

    return render_template(
        "pedido_sucesso.html",
        total="Reserva enviada",
        config=Config
    )

# ======================================================
# SOBRE
# ======================================================
@app.route("/sobre")
def sobre():

    return render_template(
        "sobre.html",
        config=Config
    )


# ======================================================
# HEALTH CHECK (🔥 FASE 2 PREPARAÇÃO SAAS)
# ======================================================
@app.route("/health")
def health():
    return {"status": "ok", "system": "restaurant-app", "version": "2.0"}


# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
