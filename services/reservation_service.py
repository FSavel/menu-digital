# ======================================================
# RESERVATION SERVICE
# Responsável pelas reservas
# ======================================================

import pandas as pd
import os


# ======================================================
# CARREGAR RESERVAS
# ======================================================
def get_reservations(file_path):

    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)

    return df.to_dict(orient="records")


# ======================================================
# ADICIONAR RESERVA
# ======================================================
def add_reservation(file, reservation):

    novo = pd.DataFrame([reservation])

    if os.path.exists(file_path):

        df = pd.read_excel(file_path)
        df = pd.concat([df, novo], ignore_index=True)

    else:

        df = novo

    df.to_excel(file_path, index=False)


# ======================================================
# ALTERAR STATUS
# ======================================================
def update_reservation_status(file_path, reservation_id, novo_status):

    if not os.path.exists(file_path):
        return False

    df = pd.read_excel(file_path)

    if "id" not in df.columns:
        return False

    mask = df["id"].astype(str) == str(reservation_id)

    if not mask.any():
        return False

    df.loc[mask, "status"] = novo_status

    df.to_excel(file_path, index=False)

    return True


# ======================================================
# APAGAR RESERVA
# ======================================================
def delete_reservation(file_path, reservation_id):

    if not os.path.exists(file_path):
        return False

    df = pd.read_excel(file_path)

    if "id" not in df.columns:
        return False

    df = df[df["id"].astype(str) != str(reservation_id)]

    df.to_excel(file_path, index=False)

    return True
