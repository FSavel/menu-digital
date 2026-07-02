# ======================================================
# TABLE SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

from services.google_service import read_sheet, write_sheet, append_row

# Nome da aba no Google Sheets
SHEET_NAME = "Mesas"


# ======================================================
# LISTAR MESAS
# ======================================================
def get_tables(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Table Service] erro ao listar mesas:", e)
        return []


# ======================================================
# OBTER UMA MESA
# ======================================================
def get_table(table_id):

    try:
        tables = get_tables()

        for table in tables:
            if str(table.get("id")) == str(table_id):
                return table

        return None

    except Exception as e:
        print("[Table Service] erro get_table:", e)
        return None


# ======================================================
# ADICIONAR MESA
# ======================================================
def add_table(file, table):

    try:
        return append_row(SHEET_NAME, table)

    except Exception as e:
        print("[Table Service] erro ao adicionar mesa:", e)
        return False


# ======================================================
# ATUALIZAR STATUS DA MESA
# ======================================================
def update_table_status(file_path, table_id, status):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        mask = df["id"] == str(table_id)

        if not mask.any():
            return False

        df.loc[mask, "status"] = status

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Table Service] erro update status:", e)
        return False


# ======================================================
# ATRIBUIR CLIENTE
# ======================================================
def assign_customer(file_path, table_id, customer_name):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        mask = df["id"] == str(table_id)

        if not mask.any():
            return False

        df.loc[mask, "cliente"] = customer_name
        df.loc[mask, "status"] = "Ocupada"

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Table Service] erro assign customer:", e)
        return False


# ======================================================
# LIBERTAR MESA
# ======================================================
def free_table(file_path, table_id):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        mask = df["id"] == str(table_id)

        if not mask.any():
            return False

        df.loc[mask, "cliente"] = ""
        df.loc[mask, "status"] = "Livre"

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Table Service] erro free table:", e)
        return False


# ======================================================
# ESTATÍSTICAS
# ======================================================
def table_stats(file_path=None):

    try:
        tables = get_tables()

        total = len(tables)
        ocupadas = len([t for t in tables if t.get("status") == "Ocupada"])
        livres = len([t for t in tables if t.get("status") == "Livre"])

        return {
            "total": total,
            "ocupadas": ocupadas,
            "livres": livres
        }

    except Exception as e:
        print("[Table Service] erro stats:", e)
        return {
            "total": 0,
            "ocupadas": 0,
            "livres": 0
        }
