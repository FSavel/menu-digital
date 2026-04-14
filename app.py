from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import os

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
# FAZER PEDIDO
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():
    nome = request.form.get("nome")
    pedido_texto = request.form.get("pedido")

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
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
    body{
        margin:0;
        font-family: Arial;
        background:#111;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        text-align:center;
    }

    button{
        margin-top:20px;
        padding:12px 20px;
        border:none;
        border-radius:8px;
        background:#27ae60;
        color:white;
        font-size:16px;
    }
    </style>

    </head>

    <body>

    <div>
        <h2>✅ Pedido enviado com sucesso!</h2>
        <p>Obrigado pela sua preferência 🍽️</p>

        <a href="/menu_pt">
        <button>Voltar ao Menu</button>
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
    <h2>🙋 Garçom chamado!</h2>
    <a href="/">Voltar</a>
    """

# =========================
# PAINEL DE PEDIDOS (COZINHA)
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
# MARCAR COMO ENTREGUE
# =========================
@app.route("/entregar/<int:id>")
def entregar(id):
    try:
        df = pd.read_excel("pedidos.xlsx")

        if id < len(df):
            df.at[id, "status"] = "Entregue"

        df.to_excel("pedidos.xlsx", index=False)

        return redirect("/pedidos")

    except:
        return "Erro ao atualizar pedido"

# =========================
# RUN (RENDER)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
