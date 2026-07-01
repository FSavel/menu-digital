# ======================================================
# ORDER SERVICE - GOOGLE SHEETS VERSION
# ======================================================

from services.google_service import read_sheet, write_sheet
from utils.helpers import gerar_id, moeda, hora_mocambique

SHEET_NAME = "Orders"


# ======================================================
# ADICIONAR PEDIDO
# ======================================================
def add_order(file_path, cliente, cart, hora):

    try:

        df = read_sheet(SHEET_NAME)

        if df is None:
            df = []

        pedido_id = gerar_id()

        # calcular total
        total = 0

        for item in cart:
            total += float(item.get("preco", 0)) * int(item.get("quantidade", 1))

        novo_pedido = {
            "id": pedido_id,
            "cliente": cliente,
            "itens": str(cart),  # guardamos JSON como string
            "total": total,
            "hora": hora,
            "status": "Recebido"
        }

        df.append(novo_pedido)

        write_sheet(SHEET_NAME, df)

        return total

    except Exception as e:
        print("Erro ao adicionar pedido:", e)
        return 0


# ======================================================
# OBTER TODOS OS PEDIDOS
# ======================================================
def get_orders(file_path=None):

    try:
        df = read_sheet(SHEET_NAME)

        if not df:
            return []

        return df

    except Exception as e:
        print("Erro ao obter pedidos:", e)
        return []


# ======================================================
# ÚLTIMOS PEDIDOS
# ======================================================
def get_last_orders(file_path=None, quantidade=10):

    pedidos = get_orders()

    return list(reversed(pedidos))[:quantidade]


# ======================================================
# STATS DASHBOARD
# ======================================================
def get_dashboard_stats(file_path=None):

    pedidos = get_orders()

    total = 0
    count = len(pedidos)

    for p in pedidos:
        try:
            total += float(p.get("total", 0))
        except:
            pass

    return {
        "total_pedidos": count,
        "total_vendas": total
    }


# ======================================================
# ATUALIZAR STATUS
# ======================================================
def update_order_status(file_path, pedido_id, novo_status):

    try:
        df = read_sheet(SHEET_NAME)

        updated = False

        for row in df:
            if str(row.get("id")) == str(pedido_id):
                row["status"] = novo_status
                updated = True

        if updated:
            write_sheet(SHEET_NAME, df)

        return updated

    except Exception as e:
        print("Erro ao atualizar status:", e)
        return False


# ======================================================
# OBTER POR ID
# ======================================================
def get_order_by_id(file_path, pedido_id):

    pedidos = get_orders()

    for p in pedidos:
        if str(p.get("id")) == str(pedido_id):
            return p

    return None


# ======================================================
# DELETE (opcional futuro)
# ======================================================
def delete_order(file_path, pedido_id):

    try:
        df = read_sheet(SHEET_NAME)

        new_df = []

        for row in df:
            if str(row.get("id")) != str(pedido_id):
                new_df.append(row)

        write_sheet(SHEET_NAME, new_df)

        return True

    except Exception as e:
        print("Erro ao eliminar pedido:", e)
        return False


# ======================================================
# TOTAL VENDAS
# ======================================================
def get_total_sales(file_path=None):

    pedidos = get_orders()

    total = 0

    for p in pedidos:
        try:
            total += float(p.get("total", 0))
        except:
            pass

    return total
