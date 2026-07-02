# ======================================================
# GOOGLE SHEETS SERVICE (PRODUÇÃO LIMPA)
# ======================================================

import os
import json
import pandas as pd
import gspread
import logging
from google.oauth2.service_account import Credentials

# ======================================================
# SCOPES
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ======================================================
# SPREADSHEET ID (IMPORTANTE - RENDER ENV)
# ======================================================

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")


# ======================================================
# CREDENCIAIS
# ======================================================

def get_credentials():

    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS_JSON não definida no ambiente")

    try:
        creds_dict = json.loads(creds_json)

        return Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )

    except Exception as e:
        raise Exception(f"Erro ao carregar credenciais Google: {e}")


# ======================================================
# CLIENT
# ======================================================

def get_client():
    return gspread.authorize(get_credentials())


# ======================================================
# ABRIR WORKSHEET CORRETO
# ======================================================

def open_sheet(sheet_name):

    if not SPREADSHEET_ID:
        raise Exception("GOOGLE_SHEETS_ID não definida no ambiente")

    client = get_client()

    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    worksheet = spreadsheet.worksheet(sheet_name)

    return worksheet


# ======================================================
# LER DADOS
# ======================================================

def read_sheet(sheet_name):

    try:
        worksheet = open_sheet(sheet_name)

        data = worksheet.get_all_records()

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(data)

    except Exception as e:
        logging.error(f"[Google Sheets] erro leitura {sheet_name}: {e}")
        return pd.DataFrame()


# ======================================================
# ESCREVER DADOS
# ======================================================

def write_sheet(sheet_name, df):

    try:
        worksheet = open_sheet(sheet_name)

        worksheet.clear()

        if df.empty:
            return True

        data = [df.columns.values.tolist()] + df.values.tolist()

        worksheet.update(data)

        return True

    except Exception as e:
        logging.error(f"[Google Sheets] erro escrita {sheet_name}: {e}")
        return False


# ======================================================
# APPEND LINHA (SEGURO)
# ======================================================

def append_row(sheet_name, row_dict):

    try:
        worksheet = open_sheet(sheet_name)

        headers = worksheet.row_values(1)

        row = [row_dict.get(col, "") for col in headers]

        worksheet.append_row(row)

        return True

    except Exception as e:
        logging.error(f"[Google Sheets] erro append: {e}")
        return False


# ======================================================
# TESTE DE CONEXÃO
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
