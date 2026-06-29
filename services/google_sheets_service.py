# ======================================================
# GOOGLE SHEETS SERVICE (FASE 3 - SaaS CORE)
# ======================================================

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import uuid

from config import Config


# ======================================================
# AUTENTICAÇÃO
# ======================================================
def get_client():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        Config.GOOGLE_CREDENTIALS_FILE,
        scopes=scope
    )

    return gspread.authorize(creds)


# ======================================================
# ABRIR SHEET
# ======================================================
def open_sheet(sheet_name):

    client = get_client()
    sheet = client.open(Config.NOME_PLANILHA).worksheet(sheet_name)

    return sheet


# ======================================================
# GERAR ID
# ======================================================
def gerar_id():
    return str(uuid.uuid4())


# ======================================================
# LER TODOS OS DADOS
# ======================================================
def get_all(sheet_name):

    sheet = open_sheet(sheet_name)
    data = sheet.get_all_records()

    return data


# ======================================================
# ADICIONAR LINHA
# ======================================================
def append_row(sheet_name, row: dict):

    sheet = open_sheet(sheet_name)

    sheet.append_row(list(row.values()))

    return True


# ======================================================
# MENU
# ======================================================
def get_menu():

    return get_all(Config.ABA_MENU)


# ======================================================
# PEDIDOS - CRIAR
# ======================================================
def create_order(nome, pedido, total, hora):

    new_order = {
        "id": gerar_id(),
        "nome": nome,
        "pedido": pedido,
        "total": total,
        "hora": hora,
        "status": "Recebido"
    }

    append_row(Config.ABA_PEDIDOS, new_order)

    return new_order["id"]


# ======================================================
# PEDIDOS - LISTAR
# ======================================================
def get_orders():

    return get_all(Config.ABA_PEDIDOS)


# ======================================================
# ATUALIZAR STATUS
# ======================================================
def update_status(order_id, new_status):

    sheet = open_sheet(Config.ABA_PEDIDOS)
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):  # linha 1 = header
        if str(row.get("id")) == str(order_id):
            sheet.update_cell(i, 5, new_status)  # coluna status
            return True

    return False


# ======================================================
# RESERVAS
# ======================================================
def create_reservation(data: dict):

    data["id"] = gerar_id()
    data["hora"] = datetime.now().isoformat()
    data["status"] = "Pendente"

    append_row(Config.ABA_RESERVAS, data)

    return data["id"]


# ======================================================
# CHAMADAS
# ======================================================
def create_call(nome="Mesa"):

    call = {
        "id": gerar_id(),
        "nome": nome,
        "pedido": "Chamada de garçom",
        "hora": datetime.now().isoformat(),
        "status": "Nova chamada"
    }

    append_row(Config.ABA_CHAMADAS, call)

    return call["id"]