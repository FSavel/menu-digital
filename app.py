from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# =========================
# CARREGAR MENU
# =========================
def carregar_menu():
    try:
        df = pd.read_excel("menu.xlsx")
        return df.to_dict(orient="records")
    except:
        return []

# =========================
# PÁGINA INICIAL (IDIOMA)
# =========================
@app.route("/")
def idioma():
    return render_template("idioma.html")

# =========================
# MENU PORTUGUÊS
# =========================
@app.route("/menu_pt")
def menu_pt():
    menu = carregar_menu()
    return render_template("menu_pt.html", menu=menu)

# =========================
# MENU INGLÊS
# =========================
@app.route("/menu_en")
def menu_en():
    menu = carregar_menu()
    return render_template("menu_en.html", menu=menu)

# =========================
# FAZER PEDIDO
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():
    nome = request.form.get("nome")
    pedido = request.form.get("pedido")

    novo = pd.DataFrame([{
        "nome": nome,
        "pedido": pedido,
        "hora": datetime.now()
    }])

    ficheiro = "pedidos.xlsx"

    if os.path.exists(ficheiro):
        df = pd.read_excel(ficheiro)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_excel(ficheiro, index=False)

    return """
    <h2>✅ Pedido enviado com sucesso!</h2>
    <a href="/">Voltar ao início</a>
    """

# =========================
# CHAMAR ATENDENTE
# =========================
@app.route("/chamar")
def chamar():
    return """
    <h2>🙋‍♂️ Atendente chamado!</h2>
    <a href="/">Voltar ao início</a>
    """

# =========================
# RUN (IMPORTANTE PARA RENDER)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)