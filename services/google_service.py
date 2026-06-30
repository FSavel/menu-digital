# ======================================================
# GOOGLE SHEETS SERVICE (PRODUÇÃO)
# ======================================================

import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ======================================================
# SCOPES (permissões Google Sheets)
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ======================================================
# CARREGAR CREDENCIAIS (ENVIRONMENT VARIABLE)
# ======================================================

def get_credentials():

    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS_JSON não definida no ambiente")

    try:
        creds_dict = json.loads(creds_json)

        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )

        return credentials

    except Exception as e:
        raise Exception(f"Erro ao carregar credenciais Google: {e}")


# ======================================================
# CLIENT GOOGLE SHEETS
# ======================================================

def get_client():

    credentials = get_credentials()

    client = gspread.authorize(credentials)

    return client


# ======================================================
# ABRIR SHEET POR NOME
# ======================================================

def open_sheet(sheet_name, worksheet_index=0):

    client = get_client()

    sheet = client.open(sheet_name)

    worksheet = sheet.get_worksheet(worksheet_index)

    return worksheet


# ======================================================
# LER DADOS (PRINCIPAL)
# ======================================================

def read_sheet(sheet_name):

    try:
        worksheet = open_sheet(sheet_name)

        data = worksheet.get_all_records()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        return df

    except Exception as e:
        print(f"[Google Sheets] Erro ao ler sheet {sheet_name}: {e}")
        return pd.DataFrame()


# ======================================================
# ESCREVER DADOS (SUBSTITUI TABELA)
# ======================================================

def write_sheet(sheet_name, df):

    try:
        worksheet = open_sheet(sheet_name)

        worksheet.clear()

        if df.empty:
            return True

        # converter DataFrame para lista
        data = [df.columns.values.tolist()] + df.values.tolist()

        worksheet.update(data)

        return True

    except Exception as e:
        print(f"[Google Sheets] Erro ao escrever sheet {sheet_name}: {e}")
        return False


# ======================================================
# ADICIONAR UMA LINHA (UTIL PARA PEDIDOS / RESERVAS)
# ======================================================

def append_row(sheet_name, row_dict):

    try:
        worksheet = open_sheet(sheet_name)

        row = list(row_dict.values())

        worksheet.append_row(row)

        return True

    except Exception as e:
        print(f"[Google Sheets] Erro ao adicionar linha: {e}")
        return False


# ======================================================
# UTILITÁRIO: VERIFICAR CONEXÃO
# ======================================================

def test_connection(sheet_name):

    try:
        df = read_sheet(sheet_name)
        return {
            "status": "ok",
            "rows": len(df)
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
