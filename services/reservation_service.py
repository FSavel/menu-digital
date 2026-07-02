# ======================================================
# RESERVATION SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

from services.google_service import read_sheet, append_row, write_sheet

# Nome da aba no Google Sheets
SHEET_NAME = "Reservas"


# ======================================================
# LISTAR RESERVAS
# ======================================================
def get_reservations(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Reservation Service] erro ao listar reservas:", e)
        return []


# ======================================================
# ADICIONAR RESERVA
# ======================================================
def add_reservation(file, reservation):

    try:
        return append_row(SHEET_NAME, reservation)

    except Exception as e:
        print("[Reservation Service] erro ao adicionar reserva:", e)
        return False


# ======================================================
# ATUALIZAR STATUS
# ======================================================
def update_reservation_status(file_path, reservation_id, novo_status):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        mask = df["id"] == str(reservation_id)

        if not mask.any():
            return False

        df.loc[mask, "status"] = novo_status

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Reservation Service] erro update status:", e)
        return False


# ======================================================
# APAGAR RESERVA
# ======================================================
def delete_reservation(file_path, reservation_id):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        df = df[df["id"] != str(reservation_id)]

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Reservation Service] erro delete:", e)
        return False
