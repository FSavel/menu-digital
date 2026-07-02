# ======================================================
# CALL SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

from services.google_service import read_sheet, append_row, write_sheet

# Nome da aba no Google Sheets
SHEET_NAME = "Chamadas"


# ======================================================
# ADICIONAR CHAMADA
# ======================================================
def add_call(file, call):

    try:
        return append_row(SHEET_NAME, call)

    except Exception as e:
        print("[Call Service] erro ao adicionar chamada:", e)
        return False


# ======================================================
# LISTAR CHAMADAS
# ======================================================
def get_calls(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Call Service] erro ao carregar chamadas:", e)
        return []


# ======================================================
# APAGAR CHAMADA
# ======================================================
def delete_call(file_path, call_id):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty or "id" not in df.columns:
            return False

        df = df[df["id"].astype(str) != str(call_id)]

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Call Service] erro ao apagar chamada:", e)
        return False


# ======================================================
# TOTAL DE CHAMADAS
# ======================================================
def total_calls(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return 0

        return len(df)

    except Exception as e:
        print("[Call Service] erro total chamadas:", e)
        return 0
