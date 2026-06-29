import pandas as pd
import os


# ======================================================
# CARREGAR CHAMADAS
# ======================================================
def load_calls(file_path):

    if os.path.exists(file_path):
        return pd.read_excel(file_path)

    return pd.DataFrame()


# ======================================================
# ADICIONAR CHAMADA
# ======================================================
def add_call(file_path, chamada):

    df = load_calls(file_path)

    novo = pd.DataFrame([chamada])

    if df.empty:
        df = novo
    else:
        df = pd.concat([df, novo], ignore_index=True)

    df.to_excel(file_path, index=False)


# ======================================================
# LISTAR CHAMADAS
# ======================================================
def get_calls(file_path):

    df = load_calls(file_path)

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ======================================================
# APAGAR CHAMADA
# ======================================================
def delete_call(file_path, call_id):

    df = load_calls(file_path)

    if df.empty:
        return False

    if "id" not in df.columns:
        return False

    df = df[df["id"] != call_id]

    df.to_excel(file_path, index=False)

    return True


# ======================================================
# TOTAL CHAMADAS
# ======================================================
def total_calls(file_path):

    df = load_calls(file_path)

    return len(df)