# ======================================================
# ORDER SERVICE (GOOGLE SHEETS ONLY)
# ======================================================
import pandas as pd
from services.google_service import read_sheet, append_row, write_sheet
from utils.helpers import gerar_id  # Importa o nosso gerador de ID único curto

# Fallback caso o nome da aba não venha por parâmetro
DEFAULT_SHEET_NAME = "Pedidos"


# ======================================================
# ADICIONAR PEDIDO (MAPEADO PARA AS COLUNAS DO SHEET)
# ======================================================
def add_order(sheet_name, cliente, cart, hora):
    try:
        # Garante o uso do nome correto da aba enviado pelo app.py
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME

        def _num(value):
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0

        def _price(item):
            return _num(item.get("price", item.get("preco", 0)))

        def _qty(item):
            return int(_num(item.get("qty", item.get("quantidade", 1))))

        def _name(item):
            return item.get("name", item.get("nome", ""))

        # Monta o resumo descritivo
        resumo = ", ".join(
            f"{_qty(item)}x {_name(item)}" for item in cart
        )

        total = sum(_price(item) * _qty(item) for item in cart)

        # Criamos o dicionário com suporte tanto para chaves antigas como novas
        # para que o 'append_row' preencha qualquer coluna presente na folha!
        # ID único alfanumérico gerado pelo nosso helper para evitar colisões de horário
        pedido = {
            "id": gerar_id(),
            "nome": cliente,
            "pedido": resumo,
            "hora": hora,
            "status": "Recebido",
            "total": total
        }

        return append_row(aba, pedido)

    except Exception as e:
        print("[Order Service] erro ao adicionar pedido:", e)
        return False

# ======================================================
# LISTAR PEDIDOS
# ======================================================
def get_orders(sheet_name=None):
    try:
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME
        df = read_sheet(aba)

        if df.empty:
            return []

        # Garante que o ID e o status sejam sempre tratados como String pura
        if "id" in df.columns:
            df["id"] = df["id"].astype(str)
        if "status" in df.columns:
            df["status"] = df["status"].astype(str)

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Order Service] erro ao carregar pedidos:", e)
        return []


# ======================================================
# ÚLTIMOS PEDIDOS
# ======================================================
def get_last_orders(sheet_name=None, quantidade=10):
    try:
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME
        pedidos = get_orders(aba)

        # Ordena cronologicamente do mais recente para o mais antigo
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
def update_order_status(sheet_name, pedido_id, novo_status):
    try:
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME
        df = read_sheet(aba)

        if df.empty:
            return False

        df["id"] = df["id"].astype(str)
        mask = df["id"] == str(pedido_id)

        if not mask.any():
            print(f"[Order Service] Pedido ID {pedido_id} não encontrado para atualização.")
            return False

        df.loc[mask, "status"] = str(novo_status)

        return write_sheet(aba, df)

    except Exception as e:
        print("[Order Service] erro status:", e)
        return False


# ======================================================
# TOTAL DO DIA
# ======================================================
def get_total_sales(sheet_name=None):
    try:
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME
        df = read_sheet(aba)

        if df.empty or "total" not in df.columns:
            return 0.0

        # Força a conversão da coluna total para numérico antes de somar
        # para evitar problemas de concatenação de strings textuais do Sheets
        totais_numericos = pd.to_numeric(df["total"], errors='coerce').fillna(0)
        return float(totais_numericos.sum())

    except Exception as e:
        print("[Order Service] erro total vendas:", e)
        return 0.0


# ======================================================
# STATS DO DASHBOARD (CORRIGIDO PARA GOOGLE SHEETS)
# ======================================================
def get_dashboard_stats(sheet_name=None):
    try:
        aba = sheet_name if sheet_name else DEFAULT_SHEET_NAME
        pedidos = get_orders(aba)
        
        total_vendas = get_total_sales(aba)

        return {
            "total_pedidos": len(pedidos),
            "total_dia": total_vendas
        }
    except Exception as e:
        print("[Order Service] erro nas estatísticas do dashboard:", e)
        return {
            "total_pedidos": 0,
            "total_dia": 0.0
        }
        
# ======================================================
# RESERVAS
# ======================================================
def get_reservations():
    try:
        # Lê especificamente a aba "Reservas" do teu Sheets
        df = read_sheet("Reservas")
        if df.empty:
            return []
        return df.to_dict(orient="records")
    except Exception as e:
        print("[Reservation Service] erro ao carregar reservas:", e)
        return []

# ======================================================
# LISTAR RESERVAS
# ======================================================
def get_reservations(sheet_name=None):
    try:
        from config import Config
        aba = sheet_name if sheet_name else "Reservas"
        df = read_sheet(aba)
        if df.empty:
            return []
        
        # Garante que o ID é tratado como String
        if "id" in df.columns:
            df["id"] = df["id"].astype(str)
            
        return df.to_dict(orient="records")
    except Exception as e:
        print("[Order Service] erro ao carregar reservas:", e)
        return []
