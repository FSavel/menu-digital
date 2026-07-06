# ======================================================
# IMPORTS
# ======================================================
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
import os

from config import Config
from languages import LANGUAGES

from utils.helpers import hora_mocambique, gerar_id

# SERVICES (GOOGLE SHEETS ONLY)
from services.menu_service import load_menu
from services.order_service import (
    add_order,
    get_orders,
    get_last_orders,
    get_dashboard_stats,
    update_order_status,
    get_total_sales
)

from services.reservation_service import (
    add_reservation,
    get_reservations
)

from services.call_service import (
    add_call,
    get_calls
)

# ======================================================
# APP
# ======================================================
app = Flask(__name__)
app.secret_key = "restaurante_secret_key"


# ======================================================
# HELPERS
# ======================================================
def get_language(lang):
    if lang not in LANGUAGES:
        lang = "pt"
    return LANGUAGES[lang]


def admin_required_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


# ======================================================
# HOME
# ======================================================
@app.route("/")
def index():

    return render_template("welcome.html")


# ======================================================
# MENU
# ======================================================
@app.route("/menu_pt")
def menu_pt():
    session["lang"] = "pt"
    return render_template("menu.html", menu=load_menu(), lang="pt", config=Config)


@app.route("/menu_en")
def menu_en():
    session["lang"] = "en"
    return render_template("menu.html", menu=load_menu(), lang="en", config=Config)


@app.route("/set_language/<lang>")
def set_language(lang):
    if lang not in ["pt", "en"]:
        lang = "pt"

    session["lang"] = lang

    return redirect(url_for("menu_en" if lang == "en" else "menu_pt"))


# ======================================================
# PEDIDO (CART)
# ======================================================
@app.route("/pedido", methods=["POST"])
def pedido():

@app.route("/pedido", methods=["POST"])
def pedido():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Pedido inválido"
        }), 400

    cart = data.get("cart", [])

    if not cart:
        return jsonify({
            "success": False,
            "error": "Carrinho vazio"
        }), 400

    total = 0

    for item in cart:
        total += item.get("price", 0) * item.get("qty", 1)

    add_order(
        Config.SHEET_ORDERS,
        "Cliente",
        cart,
        hora_mocambique()
    )

    return jsonify({
        "success": True,
        "total": total
    })

@app.route("/cart")
def cart():

    return render_template(
        "cart.html",
        config=Config,
        lang=session.get("lang", "pt")
    )
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

    add_call(Config.SHEET_CALLS, chamada)

    flash("Garçom chamado com sucesso!", "success")
    return redirect(url_for("menu_pt"))


# ======================================================
# RESERVA
# ======================================================
@app.route("/reserva", methods=["GET", "POST"])
def reserva():

    if request.method == "GET":
        return render_template("reserva.html", config=Config)

    novo = {
        "id": gerar_id(),
        "nome": request.form.get("nome"),
        "contacto": request.form.get("contacto"),
        "tipo": request.form.get("tipo"),
        "descricao": request.form.get("descricao"),
        "quantidade": request.form.get("quantidade"),
        "data": request.form.get("data"),
        "observacoes": request.form.get("observacoes"),
        "hora": hora_mocambique(),
        "status": "Pendente"
    }

    # ✅ CORREÇÃO CRÍTICA: agora usa Google Sheets corretamente
    add_reservation(Config.SHEET_RESERVATIONS, novo)

    return render_template(
        "pedido_sucesso.html",
        total="Reserva enviada",
        config=Config
    )


# ======================================================
# ADMIN LOGIN
# ======================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "GET":
        return render_template("admin/login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        flash("Login efetuado com sucesso!", "success")
        return redirect(url_for("pedidos"))

    flash("Credenciais inválidas!", "danger")
    return redirect(url_for("admin_login"))


# ======================================================
# ADMIN LOGOUT
# ======================================================
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Sessão terminada!", "info")
    return redirect(url_for("admin_login"))


# ======================================================
# PEDIDOS (ADMIN)
# ======================================================
@app.route("/pedidos")
def pedidos():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pedidos = get_orders(Config.SHEET_ORDERS)

    total_dia = get_total_sales(Config.SHEET_ORDERS)

    return render_template(
        "pedidos.html",
        pedidos=pedidos,
        total_dia=total_dia,
        config=Config
    )


# ======================================================
# COZINHA
# ======================================================
@app.route("/cozinha")
def cozinha():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pedidos = list(reversed(get_orders(Config.SHEET_ORDERS)))

    return render_template(
        "cozinha.html",
        pedidos=pedidos,
        config=Config,
        refresh_time=Config.AUTO_REFRESH_ADMIN
    )

# ======================================================
# Contador de pedidos
# ======================================================
@app.route("/api/pedidos/count")
def pedidos_count():

    pedidos = get_orders(Config.SHEET_ORDERS)

    return {
        "count": len(pedidos)
    }
# ======================================================
# Actualizacao de pedidos
# ======================================================    
@app.route("/api/pedidos")
def api_pedidos():

    pedidos = get_orders(Config.SHEET_ORDERS)

    return {
        "pedidos": pedidos
    }    
# ======================================================
# UPDATE STATUS
# ======================================================
@app.route("/api/pedido/status", methods=["POST"])
def api_update_status():

    if not session.get("admin_logged_in"):
        return {"error": "unauthorized"}, 401

    data = request.json

    update_order_status(
        Config.SHEET_ORDERS,
        data.get("id"),
        data.get("status")
    )

    return {"success": True}


# ======================================================
# HEALTH CHECK
# ======================================================
@app.route("/health")
def health():
    return {
        "status": "ok",
        "system": "restaurant-app",
        "version": Config.VERSAO
    }

# ======================================================
# Sobre
# ======================================================
@app.route("/sobre")
def sobre():
    return render_template("sobre.html", config=Config)
    
# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
