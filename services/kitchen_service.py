import pandas as pd
import os


# ======================================================
# CARREGAR PEDIDOS
# ======================================================
def load_orders(file_path):

    if os.path.exists(file_path):
        return pd.read_excel(file_path)

    return pd.DataFrame()


# ======================================================
# PEDIDOS DA COZINHA
# ======================================================
def kitchen_orders(file_path):

    df = load_orders(file_path)

    if df.empty:
        return []

    # mais recentes primeiro
    df = df.iloc[::-1]

    return df.to_dict(orient="records")


# ======================================================
# PEDIDOS RECEBIDOS
# ======================================================
def received_orders(file_path):

    df = load_orders(file_path)

    if df.empty:
        return []

    return df[df["status"] == "Recebido"].to_dict(orient="records")


# ======================================================
# EM PREPARAÇÃO
# ======================================================
def preparing_orders(file_path):

    df = load_orders(file_path)

    if df.empty:
        return []

    return df[df["status"] == "Em Preparação"].to_dict(orient="records")


# ======================================================
# PRONTOS
# ======================================================
def ready_orders(file_path):

    df = load_orders(file_path)

    if df.empty:
        return []

    return df[df["status"] == "Pronto"].to_dict(orient="records")


# ======================================================
# ENTREGUES
# ======================================================
def delivered_orders(file_path):

    df = load_orders(file_path)

    if df.empty:
        return []

    return df[df["status"] == "Entregue"].to_dict(orient="records")


# ======================================================
# CONTADORES
# ======================================================
def kitchen_stats(file_path):

    df = load_orders(file_path)

    if df.empty:

        return {

            "recebidos": 0,
            "preparacao": 0,
            "prontos": 0,
            "entregues": 0
        }

    return {

        "recebidos": len(df[df["status"] == "Recebido"]),

        "preparacao": len(df[df["status"] == "Em Preparação"]),

        "prontos": len(df[df["status"] == "Pronto"]),

        "entregues": len(df[df["status"] == "Entregue"])
    }