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
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "restaurante_secret_key")


# ======================================================
# HELPERS
# ======================================================
def get_language_dict():
    lang = session.get("lang", "pt")
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
# HOME / WELCOME PAGE (CORRIGIDO)
# ======================================================
@app.route("/")
def index():
    # Força sempre a exibição da Welcome Page Premium para escolha de idioma,
    # garantindo que o fluxo inicial do QR Code nunca seja ignorado.
    return render_template("welcome.html", config=Config)


# ======================================================
# IDIOMA ROTAS
# ======================================================
@app.route("/set_language/<lang>")
def set_language(lang):
    if lang not in Config.IDIOMAS:
        lang = "pt"

    session["lang"] = lang
    return redirect(url_for("menu"))


# ======================================================
# MENU DIGITAL (UNIFICADO)
# ======================================================
@app.route("/menu")
def menu():
    # Garante que existe um idioma padrão na sessão caso o utilizador tente aceder direto à rota
    if "lang" not in session:
        session["lang"] = "pt"
        
    lang = session["lang"]
    textos = get_language_dict()
    
    return render_template(
        "menu.html", 
        menu=load_menu(), 
        lang=lang, 
        textos=textos, 
        config=Config,
        refresh_time=Config.AUTO_REFRESH_CLIENTE
    )


# RETROCOMPATIBILIDADE: Mantido caso existam QR Codes impressos com estas rotas antigos
@app.route("/menu_pt")
def menu_pt():
    session["lang"] = "pt"
    return redirect(url_for("menu"))


@app.route("/menu_en")
def menu_en():
    session["lang"] = "en"
    return redirect(url_for("menu"))


# ======================================================
# PEDIDO (CART - RECONSTRUTOR DINÂMICO)
# ======================================================
@app.route("/pedido", methods=["POST"])
def pedido():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Pedido inválido"
        }), 400

    # 1. Pega o carrinho original enviado pelo JS
    cart = data.get("cart", [])
    
    # 2. Pega o nome do cliente que foi digitado (se não houver, assume "Cliente")
    nome_cliente = data.get("nome") or data.get("cliente") or "Cliente"

    if not cart:
        return jsonify({
            "success": False,
            "error": "Carrinho vazio"
        }), 400

    # 3. Calcula o total para responder ao cliente
    total = 0
    for item in cart:
        total += item.get("price", 0) * item.get("qty", 1)

    # 4. Envia o nome real e o carrinho para a tua função do Google Sheets gerar os IDs e o resumo!
    add_order(
        Config.SHEET_ORDERS,
        nome_cliente,
        cart,
        hora_mocambique()
    )

    return jsonify({
        "success": True,
        "total": total

    global CACHE_PEDIDOS
    CACHE_PEDIDOS = None
    })

@app.route("/cart")
def cart():
    return render_template(
        "cart.html",
        config=Config,
        lang=session.get("lang", "pt"),
        textos=get_language_dict()
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

    return redirect(url_for("menu"))


# ======================================================
# RESERVA
# ======================================================
@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    if request.method == "GET":
        return render_template("reserva.html", config=Config, textos=get_language_dict())

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

    add_reservation(Config.SHEET_RESERVATIONS, novo)

    return render_template(
        "pedido_sucesso.html",
        total="Reserva enviada",
        config=Config,
        textos=get_language_dict()
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
    return {"count": len(pedidos)}

# ======================================================
# CACHE INTELIGENTE PARA EVITAR O ERRO 429 DO GOOGLE
# ======================================================
CACHE_PEDIDOS = None
ULTIMA_ATUALIZACAO = 0
TEMPO_CACHE = 15  # Tempo em segundos que o servidor guarda a cópia em memória

@app.route("/api/pedidos", methods=["GET"])
def api_pedidos():
    global CACHE_PEDIDOS, ULTIMA_ATUALIZACAO
    agora = time.time()

    # Se a cache estiver vazia ou já passarem 15 segundos, vai buscar dados frescos ao Google
    if CACHE_PEDIDOS is None or (agora - ULTIMA_ATUALIZACAO) > TEMPO_CACHE:
        try:
            from services.google_service import read_sheet
            from config import Config
            
            df = read_sheet(Config.SHEET_ORDERS)
            
            if df.empty:
                CACHE_PEDIDOS = []
            else:
                # Converte o DataFrame do pandas para uma lista de dicionários limpa
                CACHE_PEDIDOS = df.to_dict(orient="records")
                
            ULTIMA_ATUALIZACAO = agora
            print("[Cache] Dados atualizados diretamente do Google Sheets.")
            
        except Exception as e:
            print(f"[Cache] Erro ao ler do Google, usando dados antigos: {e}")
            if CACHE_PEDIDOS is None:
                CACHE_PEDIDOS = []

    return jsonify(CACHE_PEDIDOS)    

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
# UPDATE STATUS (LINK/GET - usado pela cozinha e admin)
# ======================================================
@app.route("/admin/pedido/status/<pedido_id>/<status>")
def admin_update_status(pedido_id, status):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if status not in Config.STATUS_PEDIDO:
        flash("Status inválido!", "danger")
        return redirect(request.referrer or url_for("cozinha"))

    update_order_status(Config.SHEET_ORDERS, pedido_id, status)
    return redirect(request.referrer or url_for("cozinha"))


# ======================================================
# DASHBOARD (ADMIN)
# ======================================================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    pedidos = list(reversed(get_orders(Config.SHEET_ORDERS)))

    def _count(status):
        return sum(1 for p in pedidos if str(p.get("status")) == status)

    stats = {
        "total_pedidos": len(pedidos),
        "total_receita": get_total_sales(Config.SHEET_ORDERS),
        "recebidos": _count("Recebido"),
        "preparacao": _count("Em Preparação"),
        "prontos": _count("Pronto"),
        "entregues": _count("Entregue"),
    }

    return render_template(
        "admin/dashboard.html",
        pedidos=pedidos,
        stats=stats,
        config=Config
    )


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
    return render_template("sobre.html", config=Config, textos=get_language_dict())
    

# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
