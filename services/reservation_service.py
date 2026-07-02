# ======================================================
# RESERVATION SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

from services.google_service import read_sheet, append_row, write_sheet

# Nome da aba no Google Sheets
SHEET_NAME = "Reservas"

# ======================================================
# CARREGAR RESERVAS
# ======================================================
def get_reservations():

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Reservation Service] erro ao carregar reservas:", e)
        return []


# ======================================================
# ADICIONAR RESERVA
# ======================================================
def add_reservation(reservation):

    try:
        return append_row(SHEET_NAME, reservation)

    except Exception as e:
        print("[Reservation Service] erro ao adicionar reserva:", e)
        return False


# ======================================================
# ALTERAR STATUS
# ======================================================
def update_reservation_status(reservation_id, novo_status):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty or "id" not in df.columns:
            return False

        df.loc[df["id"].astype(str) == str(reservation_id), "status"] = novo_status

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Reservation Service] erro ao atualizar status:", e)
        return False


# ======================================================
# APAGAR RESERVA
# ======================================================
def delete_reservation(reservation_id):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty or "id" not in df.columns:
            return False

        df = df[df["id"].astype(str) != str(reservation_id)]

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Reservation Service] erro ao apagar reserva:", e)
        return False
