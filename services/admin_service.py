import pandas as pd
import os


# ======================================================
# CARREGAR DADOS
# ======================================================
def load_data(file_path):

    if os.path.exists(file_path):
        return pd.read_excel(file_path)

    return pd.DataFrame()


# ======================================================
# TOTAL DE PEDIDOS
# ======================================================
def total_orders(file_path):

    df = load_data(file_path)

    return len(df)


# ======================================================
# RECEITA TOTAL
# ======================================================
def total_revenue(file_path):

    df = load_data(file_path)

    if df.empty:
        return 0

    if "total" not in df.columns:
        return 0

    return float(df["total"].fillna(0).sum())


# ======================================================
# CONTAR POR STATUS
# ======================================================
def count_status(file_path, status):

    df = load_data(file_path)

    if df.empty:
        return 0

    if "status" not in df.columns:
        return 0

    return len(df[df["status"] == status])


# ======================================================
# PEDIDOS RECENTES
# ======================================================
def recent_orders(file_path, quantidade=10):

    df = load_data(file_path)

    if df.empty:
        return []

    df = df.iloc[::-1]

    return df.head(quantidade).to_dict(orient="records")


# ======================================================
# DASHBOARD
# ======================================================
def dashboard(file_path):

    return {

        "total_pedidos": total_orders(file_path),

        "total_receita": total_revenue(file_path),

        "recebidos": count_status(
            file_path,
            "Recebido"
        ),

        "preparacao": count_status(
            file_path,
            "Em Preparação"
        ),

        "prontos": count_status(
            file_path,
            "Pronto"
        ),

        "entregues": count_status(
            file_path,
            "Entregue"
        )
    }


# ======================================================
# ESTATÍSTICAS COMPLETAS
# ======================================================
def statistics(file_path):

    df = load_data(file_path)

    if df.empty:

        return {

            "pedidos": 0,

            "receita": 0,

            "ticket_medio": 0,

            "recebidos": 0,

            "preparacao": 0,

            "prontos": 0,

            "entregues": 0
        }

    receita = float(df["total"].fillna(0).sum())

    pedidos = len(df)

    ticket = 0

    if pedidos > 0:
        ticket = receita / pedidos

    return {

        "pedidos": pedidos,

        "receita": receita,

        "ticket_medio": round(ticket, 2),

        "recebidos": len(df[df["status"] == "Recebido"]),

        "preparacao": len(df[df["status"] == "Em Preparação"]),

        "prontos": len(df[df["status"] == "Pronto"]),

        "entregues": len(df[df["status"] == "Entregue"])
    }