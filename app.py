from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os
import json

app = Flask(__name__)

# =========================
# MENU
# =========================
def carregar_menu():
    try:
        df = pd.read_excel("menu.xlsx")
        return df.to_dict(orient="records")
    except:
        return []

# =========================
# HOME (IDIOMA)
# =========================
@app.route("/")
def idioma():
    return render_template("idioma.html")

# =========================
# MENU PT
# =========================
@app.route("/menu_pt")
def menu_pt():
    menu = carregar_menu()
    return render_template("menu_pt.html", menu=menu)

# =========================
# MENU EN
# =========================
@app.route("/menu_en")
def menu_en():
    menu = carregar_menu()
    return render_template("menu_en.html", menu=menu)

# =========================
# PEDIDOS
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():

    nome = request.form.get("nome")
    pedido_raw = request.form.get("pedido")

    # 🔥 Converter JSON do carrinho em texto bonito
    try:
        pedido_lista = json.loads(pedido_raw)

        pedido_texto = " | ".join([
            f"{item['name']} x{item['qty']}"
            for item in pedido_lista
        ])

    except:
        pedido_texto = pedido_raw

    novo = pd.DataFrame([{
        "nome": nome,
        "pedido": pedido_texto,
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pendente"
    }])

    ficheiro = "pedidos.xlsx"

    if os.path.exists(ficheiro):
        df = pd.read_excel(ficheiro)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_excel(ficheiro, index=False)

    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background:#111;color:white;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center;font-family:Arial;">

        <div>
            <h2>✅ Pedido enviado com sucesso!</h2>
            <h3>✔ Order completed successfully!</h3>
            <p>Obrigado pela sua preferência 🍽️</p>

            <a href="/menu_pt">
                <button style="padding:12px;background:#27ae60;color:white;border:none;border-radius:8px;">
                    Voltar ao Menu
                </button>
            </a>
        </div>

    </body>
    </html>
    """

# =========================
# CHAMAR GARÇOM
# =========================
@app.route("/chamar")
def chamar():

    novo = pd.DataFrame([{
        "nome": "Mesa",
        "pedido": "Chamada de garçom",
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Nova chamada"
    }])

    ficheiro = "chamadas.xlsx"

    if os.path.exists(ficheiro):
        df = pd.read_excel(ficheiro)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_excel(ficheiro, index=False)

    return """
    <html>
    <body style="text-align:center;font-family:Arial;">
        <h2>🙋 Garçom chamado!</h2>
        <a href="/menu_pt"><button>Voltar</button></a>
    </body>
    </html>
    """

# =========================
# PAINEL PEDIDOS
# =========================
@app.route("/pedidos")
def ver_pedidos():
    try:
        df = pd.read_excel("pedidos.xlsx")
        pedidos = df.to_dict(orient="records")
        return render_template("pedidos.html", pedidos=pedidos)
    except:
        return "<h3>Nenhum pedido encontrado</h3>"

# =========================
# ENTREGAR PEDIDO
# =========================
@app.route("/entregar/<int:id>")
def entregar(id):

    try:
        df = pd.read_excel("pedidos.xlsx")

        if 0 <= id < len(df):
            df.at[id, "status"] = "Entregue"

        df.to_excel("pedidos.xlsx", index=False)

        return redirect("/pedidos")

    except:
        return "<h3>Erro ao atualizar pedido</h3>"

# =========================
# RESERVAS
# =========================
@app.route("/reserva", methods=["GET", "POST"])
def reserva():

    if request.method == "GET":
        return render_template("reserva.html")

    novo = pd.DataFrame([{
        "nome": request.form.get("nome"),
        "contacto": request.form.get("contacto"),
        "tipo": request.form.get("tipo"),
        "descricao": request.form.get("descricao"),
        "quantidade": request.form.get("quantidade"),
        "data": request.form.get("data"),
        "observacoes": request.form.get("observacoes"),
        "hora_registo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pendente"
    }])

    ficheiro = "reservas.xlsx"

    if os.path.exists(ficheiro):
        df = pd.read_excel(ficheiro)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_excel(ficheiro, index=False)

    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background:#111;color:white;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center;font-family:Arial;">

        <div>
            <h2>📦 Reserva enviada com sucesso!</h2>
            <h3>✔ Reservation sent successfully!</h3>
            <p>Entraremos em contacto para confirmar detalhes e pagamento.</p>

            <a href="/">
                <button style="padding:12px;background:#27ae60;color:white;border:none;border-radius:8px;">
                    Voltar
                </button>
            </a>
        </div>

    </body>
    </html>
    """

# =========================
# PAINEL RESERVAS
# =========================
@app.route("/reservas_admin")
def ver_reservas():
    try:
        df = pd.read_excel("reservas.xlsx")
        reservas = df.to_dict(orient="records")
        return render_template("reservas_admin.html", reservas=reservas)
    except:
        return "<h3>Sem reservas ainda</h3>"

# =========================
# CONFIRMAR RESERVA
# =========================
@app.route("/confirmar_reserva/<int:id>")
def confirmar_reserva(id):

    df = pd.read_excel("reservas.xlsx")

    if 0 <= id < len(df):
        df.at[id, "status"] = "Contactado"

    df.to_excel("reservas.xlsx", index=False)

    return redirect("/reservas_admin")

# =========================
# CONCLUIR RESERVA
# =========================
@app.route("/concluir_reserva/<int:id>")
def concluir_reserva(id):

    df = pd.read_excel("reservas.xlsx")

    if 0 <= id < len(df):
        df.at[id, "status"] = "Concluído"

    df.to_excel("reservas.xlsx", index=False)

    return redirect("/reservas_admin")

# =========================
# SOBRE / CONTACTO
# =========================
@app.route("/sobre")
def sobre():
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;padding:20px;">

    <h2>🍽️ Clube A3</h2>

    <h3>📞 Restaurante</h3>
    <p>+258878605154</p>

    <h3>👨‍💻 Desenvolvedor</h3>
    <p>Firmino S. Savel</p>
    <p>+258879131089 | +258844681767</p>
    <p>firminosavel@gmail.com</p>

    <h3>🗺️ Localização</h3>
    <a href="https://www.google.com/maps?q=-25.9692,32.5732" target="_blank">
        <button style="padding:12px;background:#27ae60;color:white;border:none;border-radius:8px;">
            Ver no Mapa
        </button>
    </a>

    <br><br>
    <a href="/"><button style="padding:10px;">Voltar</button></a>

    </body>
    </html>
    """

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
