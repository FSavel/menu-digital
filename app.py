from flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime
import pytz
import os
import json

app = Flask(__name__)

# =========================
# HORA MOÇAMBIQUE FORMATADA
# =========================
def hora_mocambique_bonita():
    tz = pytz.timezone("Africa/Maputo")
    agora = datetime.now(tz)

    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    dia = agora.day
    mes = meses[agora.month]
    hora = agora.strftime("%H:%M")

    return f"{dia} {mes}, {hora}"


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
# PEDIDO (COM TOTAL)
# =========================
@app.route("/pedido", methods=["POST"])
def pedido():

    nome = request.form.get("nome")
    pedido_raw = request.form.get("pedido")

    total = 0
    pedido_texto = pedido_raw

    try:
        if pedido_raw:
            pedido_lista = json.loads(pedido_raw)
        else:
            pedido_lista = []

        linhas = []

        for item in pedido_lista:
            subtotal = float(item.get("price", 0)) * int(item.get("qty", 1))
            total += subtotal
            linhas.append(f"{item.get('name')} x{item.get('qty')}")

        if linhas:
            pedido_texto = " | ".join(linhas)

    except:
        pedido_texto = pedido_raw

    novo = pd.DataFrame([{
        "nome": nome,
        "pedido": pedido_texto,
        "total": total,
        "hora": hora_mocambique_bonita(),
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
        "pedido": "🙋 Chamada de garçom",
        "hora": hora_mocambique_bonita(),
        "status": "Nova chamada"
    }])

    ficheiro = "chamadas.xlsx"

    if os.path.exists(ficheiro):
        df = pd.read_excel(ficheiro)
        df = pd.concat([df, novo], ignore_index=True)
    else:
        df = novo

    df.to_excel(ficheiro, index=False)

    return redirect("/menu_pt")


# =========================
# PAINEL PEDIDOS
# =========================
@app.route("/pedidos")
def ver_pedidos():

    try:
        df = pd.read_excel("pedidos.xlsx")
        pedidos = df.to_dict(orient="records")

        total_dia = df["total"].fillna(0).sum() if "total" in df.columns else 0

        return render_template("pedidos.html",
                               pedidos=pedidos,
                               total_dia=total_dia)

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
        "hora_registo": hora_mocambique_bonita(),
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
# SOBRE / CONTACTO / MAPA
# =========================
@app.route("/sobre")
def sobre():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="
        margin:0;
        background:#111;
        color:white;
        font-family:Arial;
        display:flex;
        justify-content:center;
        align-items:center;
        min-height:100vh;
        padding:20px;
    ">

    <div style="
        width:100%;
        max-width:500px;
        background:rgba(255,255,255,0.05);
        padding:20px;
        border-radius:12px;
        line-height:1.6;
        font-size:16px;
    ">

        <h2 style="text-align:center;">🍽️ Dourados</h2>

        <hr style="border:0;border-top:1px solid #444;margin:15px 0;">

        <h3>📞 Restaurante</h3>
        <p style="font-size:18px;">+258878605154</p>

        <h3>👨‍💻 Desenvolvedor</h3>
        <p>Firmino S. Savel</p>

        <p style="font-size:16px;">
            +258879131089<br>
            +258844681767
        </p>

        <p style="word-break:break-word;">
            📧 firminosavel@gmail.com
        </p>

        <h3>🗺️ Localização</h3>

        <a href="https://www.google.com/maps/place/Dourados+Alojamentos,+E.I/@-25.4033605,32.8068776,17z/data=!4m14!1m7!3m6!1s0x1ee6df0047b833a7:0x80ea2da52529f9d2!2sDourados+Alojamentos,+E.I!8m2!3d-25.4033605!4d32.8068776!16s%2Fg%2F11xdwj829s!3m5!1s0x1ee6df0047b833a7:0x80ea2da52529f9d2!8m2!3d-25.4033605!4d32.8068776!16s%2Fg%2F11xdwj829s?entry=ttu&g_ep=EgoyMDI2MDQxNS4wIKXMDSoASAFQAw%3D%3D" target="_blank">
            <button style="
                width:100%;
                padding:12px;
                border:none;
                border-radius:8px;
                background:#27ae60;
                color:white;
                font-size:16px;
                margin-top:10px;
            ">
                Ver no Mapa
            </button>
        </a>

        <a href="/menu_pt">
            <button style="
                width:100%;
                padding:12px;
                border:none;
                border-radius:8px;
                background:#444;
                color:white;
                font-size:16px;
                margin-top:10px;
            ">
                Voltar
            </button>
        </a>

    </div>

    </body>
    </html>
    """


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
