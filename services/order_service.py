# ======================================================
# ORDER SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

from services.google_service import read_sheet, append_row, write_sheet

# Nome da aba no Google Sheets
SHEET_NAME = "Pedidos"


# ======================================================
# ADICIONAR PEDIDO
# ======================================================
def add_order(file, cliente, cart, hora):

    try:
        pedido = {
            "id": str(hora),
            "cliente": cliente,
            "items": str(cart),
            "hora": hora,
            "status": "Recebido",
            "total": sum(
                item.get("preco", 0) * item.get("quantidade", 1)
                for item in cart
            )
        }

        return append_row(SHEET_NAME, pedido)

    except Exception as e:
        print("[Order Service] erro ao adicionar pedido:", e)
        return False


# ======================================================
# LISTAR PEDIDOS
# ======================================================
def get_orders(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Order Service] erro ao carregar pedidos:", e)
        return []


# ======================================================
# ÚLTIMOS PEDIDOS
# ======================================================
def get_last_orders(file_path=None, quantidade=10):

    try:
        pedidos = get_orders()

        pedidos = sorted(
            pedidos,
            key=lambda x: x.get("hora", ""),
            reverse=True
        )

        return pedidos[:quantidade]

    except Exception as e:
        print("[Order Service] erro últimos pedidos:", e)
        return []


# ======================================================
# UPDATE STATUS
# ======================================================
def update_order_status(file_path, pedido_id, novo_status):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)

        mask = df["id"] == str(pedido_id)

        if not mask.any():
            return False

        df.loc[mask, "status"] = novo_status

        return write_sheet(SHEET_NAME, df)

    except Exception as e:
        print("[Order Service] erro status:", e)
        return False


# ======================================================
# TOTAL DO DIA
# ======================================================
def get_total_sales(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return 0

        if "total" not in df.columns:
            return 0

        return float(df["total"].sum())

    except Exception as e:
        print("[Order Service] erro total vendas:", e)
        return 0
