# ======================================================
# ORDER SERVICE
# Responsável por toda a lógica dos pedidos
# ======================================================

import pandas as pd
import os
import json
from utils.helpers import gerar_id


# ======================================================
# ADICIONAR PEDIDO
# ======================================================
def add_order(file_path, nome, pedido_raw, hora):

    total = 0

    pedido_texto = ""

    try:

        itens = json.loads(pedido_raw) if pedido_raw else []

        linhas = []

        for item in itens:

            preco = float(item.get("price", 0))
            quantidade = int(item.get("qty", 1))

            subtotal = preco * quantidade

            total += subtotal

            linhas.append(f"{item.get('name')} x{quantidade}")

        pedido_texto = " | ".join(linhas)

    except:

        pedido_texto = pedido_raw

    novo = pd.DataFrame([{

        "id": gerar_id(),

        "nome": nome,

        "pedido": pedido_texto,

        "total": total,

        "hora": hora,

        "status": "Recebido"

    }])

    if os.path.exists(file_path):

        df = pd.read_excel(file_path)

        df = pd.concat([df, novo], ignore_index=True)

    else:

        df = novo

    df.to_excel(file_path, index=False)

    return total


# ======================================================
# OBTER TODOS OS PEDIDOS
# ======================================================
def get_orders(file_path):

    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)

    return df.to_dict(orient="records")


# ======================================================
# ÚLTIMOS PEDIDOS
# ======================================================
def get_last_orders(file_path, quantidade=10):

    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)

    return df.tail(quantidade).to_dict(orient="records")


# ======================================================
# ESTATÍSTICAS
# ======================================================
def get_dashboard_stats(file_path):

    if not os.path.exists(file_path):

        return {
            "total_pedidos": 0,
            "total_receita": 0,
            "pendentes": 0,
            "entregues": 0
        }

    df = pd.read_excel(file_path)

    return {

        "total_pedidos": len(df),

        "total_receita": float(df["total"].fillna(0).sum()),

        "pendentes": len(df[df["status"] == "Recebido"]),

        "entregues": len(df[df["status"] == "Entregue"])
    }


# ======================================================
# ALTERAR STATUS
# ======================================================
def update_order_status(file_path, pedido_id, novo_status):

    if not os.path.exists(file_path):
        return

    df = pd.read_excel(file_path)

    df.loc[df["id"].astype(str) == str(pedido_id), "status"] = novo_status

    df.to_excel(file_path, index=False)


# ======================================================
# PROCURAR PEDIDO
# ======================================================
def get_order_by_id(file_path, pedido_id):

    if not os.path.exists(file_path):
        return None

    df = pd.read_excel(file_path)

    pedido = df[df["id"].astype(str) == str(pedido_id)]

    if pedido.empty:
        return None

    return pedido.iloc[0].to_dict()


# ======================================================
# APAGAR PEDIDO
# ======================================================
def delete_order(file_path, pedido_id):

    if not os.path.exists(file_path):
        return

    df = pd.read_excel(file_path)

    df = df[df["id"].astype(str) != str(pedido_id)]

    df.to_excel(file_path, index=False)


# ======================================================
# TOTAL DE VENDAS
# ======================================================
def get_total_sales(file_path):

    if not os.path.exists(file_path):
        return 0

    df = pd.read_excel(file_path)

    return float(df["total"].fillna(0).sum())