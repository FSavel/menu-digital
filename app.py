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
# HOME
# =========================
@app.route("/")
def idioma():
    return render_template("idioma.html")

# =========================
# MENUS
# =========================
@app.route("/menu_pt")
def menu_pt():
    return render_template("menu_pt.html", menu=carregar_menu())

@app.route("/menu_en")
def menu_en():
    return render_template("menu_en.html", menu=carregar_menu())

# =========================
# PEDIDOS (COM TOTAL)
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():

    nome = request.form.get("nome")
    pedido_raw = request.form.get("pedido")

    total = 0

    try:
        pedido_lista = json.loads(pedido_raw)

        linhas = []
        for item in pedido_lista:
            subtotal = item['price'] * item['qty']
            total += subtotal
            linhas.append(f"{item['name']} x{item['qty']}")

        pedido_texto = " | ".join(linhas)

    except:
        pedido_texto = pedido_raw

    novo = pd.DataFrame([{
        "nome": nome,
        "pedido": pedido_texto,
        "total": total,
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

    return f"""
    <html>
    <body style="background:#111;color:white;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center;font-family:Arial;">
        <div>
            <h2>✅ Pedido enviado com sucesso!</h2>
            <h3>✔ Order completed successfully!</h3>
            <h3>💰 Total: {total} MZN</h3>
            <a href="/menu_pt"><button style="padding:12px;background:#27ae60;color:white;border:none;border-radius:8px;">Voltar</button></a>
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

    return "<h2>🙋 Garçom chamado!</h2><a href='/menu_pt'>Voltar</a>"

# =========================
# PAINEL PEDIDOS (COM TOTAL DO DIA)
# =========================
@app.route("/pedidos")
def ver_pedidos():
    try:
        df = pd.read_excel("pedidos.xlsx")

        pedidos = df.to_dict(orient="records")

        # 💰 TOTAL DO DIA
        total_dia = df["total"].sum() if "total" in df.columns else 0

        return render_template("pedidos.html", pedidos=pedidos, total_dia=total_dia)

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
    <body style="background:#111;color:white;text-align:center;font-family:Arial;padding-top:40px;">
        <h2>📦 Reserva enviada com sucesso!</h2>
        <h3>✔ Reservation sent successfully!</h3>
        <a href="/"><button>Voltar</button></a>
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
# SOBRE
# =========================
@app.route("/sobre")
def sobre():
    return """
    <html>
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
            <button>Ver no Mapa</button>
        </a>

        <br><br>
        <a href="/"><button>Voltar</button></a>
    </body>
    </html>
    """

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
