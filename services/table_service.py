import os
import pandas as pd


# ======================================================
# CARREGAR MESAS
# ======================================================
def load_tables(file_path):

    if os.path.exists(file_path):
        return pd.read_excel(file_path)

    return pd.DataFrame()


# ======================================================
# GUARDAR MESAS
# ======================================================
def save_tables(file_path, df):

    df.to_excel(file_path, index=False)


# ======================================================
# LISTAR TODAS AS MESAS
# ======================================================
def get_tables(file_path):

    df = load_tables(file_path)

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ======================================================
# OBTER UMA MESA
# ======================================================
def get_table(file_path, table_id):

    df = load_tables(file_path)

    if df.empty:
        return None

    if "id" not in df.columns:
        return None

    mesa = df[df["id"] == table_id]

    if mesa.empty:
        return None

    return mesa.iloc[0].to_dict()


# ======================================================
# ADICIONAR MESA
# ======================================================
def add_table(file_path, mesa):

    df = load_tables(file_path)

    novo = pd.DataFrame([mesa])

    if df.empty:
        df = novo
    else:
        df = pd.concat([df, novo], ignore_index=True)

    save_tables(file_path, df)


# ======================================================
# ALTERAR ESTADO
# ======================================================
def update_table_status(file_path, table_id, novo_estado):

    df = load_tables(file_path)

    if df.empty:
        return False

    if "id" not in df.columns:
        return False

    index = df[df["id"] == table_id].index

    if len(index) == 0:
        return False

    df.at[index[0], "estado"] = novo_estado

    save_tables(file_path, df)

    return True


# ======================================================
# ASSOCIAR CLIENTE
# ======================================================
def assign_customer(file_path, table_id, cliente):

    df = load_tables(file_path)

    if df.empty:
        return False

    index = df[df["id"] == table_id].index

    if len(index) == 0:
        return False

    df.at[index[0], "cliente"] = cliente

    save_tables(file_path, df)

    return True


# ======================================================
# ASSOCIAR PEDIDO
# ======================================================
def assign_order(file_path, table_id, pedido_id):

    df = load_tables(file_path)

    if df.empty:
        return False

    index = df[df["id"] == table_id].index

    if len(index) == 0:
        return False

    df.at[index[0], "pedido_id"] = pedido_id

    save_tables(file_path, df)

    return True


# ======================================================
# LIBERTAR MESA
# ======================================================
def free_table(file_path, table_id):

    df = load_tables(file_path)

    if df.empty:
        return False

    index = df[df["id"] == table_id].index

    if len(index) == 0:
        return False

    df.at[index[0], "estado"] = "Livre"
    df.at[index[0], "cliente"] = ""
    df.at[index[0], "pedido_id"] = ""

    save_tables(file_path, df)

    return True


# ======================================================
# ESTATÍSTICAS
# ======================================================
def table_stats(file_path):

    df = load_tables(file_path)

    if df.empty:

        return {

            "total": 0,
            "livres": 0,
            "ocupadas": 0,
            "reservadas": 0,
            "limpeza": 0

        }

    return {

        "total": len(df),

        "livres": len(df[df["estado"] == "Livre"]),

        "ocupadas": len(df[df["estado"] == "Ocupada"]),

        "reservadas": len(df[df["estado"] == "Reservada"]),

        "limpeza": len(df[df["estado"] == "Limpeza"])

    }


# ======================================================
# LISTAR MESAS LIVRES
# ======================================================
def free_tables(file_path):

    df = load_tables(file_path)

    if df.empty:
        return []

    return df[df["estado"] == "Livre"].to_dict(orient="records")


# ======================================================
# LISTAR MESAS OCUPADAS
# ======================================================
def occupied_tables(file_path):

    df = load_tables(file_path)

    if df.empty:
        return []

    return df[df["estado"] == "Ocupada"].to_dict(orient="records")