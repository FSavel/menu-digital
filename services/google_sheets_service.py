# ======================================================
# GOOGLE SHEETS SERVICE
# ======================================================

import os
import json
import gspread
import pandas as pd

from google.oauth2.service_account import Credentials


# ======================================================
# SCOPES
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# ======================================================
# NOME DO GOOGLE SHEET
# ======================================================

GOOGLE_SHEET = "Menu Digital"


# ======================================================
# CLIENTE GOOGLE
# ======================================================

def get_client():

    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not credentials_json:
        raise Exception(
            "Environment Variable GOOGLE_CREDENTIALS_JSON não encontrada."
        )

    credentials_dict = json.loads(credentials_json)

    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=SCOPES
    )

    return gspread.authorize(credentials)


# ======================================================
# ABRIR GOOGLE SHEET
# ======================================================

def get_spreadsheet():

    client = get_client()

    return client.open(GOOGLE_SHEET)


# ======================================================
# OBTER WORKSHEET
# ======================================================

def get_worksheet(nome_folha):

    spreadsheet = get_spreadsheet()

    try:
        return spreadsheet.worksheet(nome_folha)

    except gspread.WorksheetNotFound:

        worksheet = spreadsheet.add_worksheet(
            title=nome_folha,
            rows=1000,
            cols=30
        )

        return worksheet


# ======================================================
# LER FOLHA
# ======================================================

def read_sheet(nome_folha):

    worksheet = get_worksheet(nome_folha)

    dados = worksheet.get_all_records()

    if not dados:
        return pd.DataFrame()

    return pd.DataFrame(dados)


# ======================================================
# ESCREVER DATAFRAME
# ======================================================

def write_sheet(nome_folha, dataframe):

    worksheet = get_worksheet(nome_folha)

    worksheet.clear()

    worksheet.update(
        [list(dataframe.columns)] +
        dataframe.fillna("").values.tolist()
    )


# ======================================================
# ADICIONAR LINHA
# ======================================================

def append_row(nome_folha, linha):

    worksheet = get_worksheet(nome_folha)

    worksheet.append_row(linha)


# ======================================================
# ATUALIZAR CÉLULA
# ======================================================

def update_cell(nome_folha, row, col, valor):

    worksheet = get_worksheet(nome_folha)

    worksheet.update_cell(row, col, valor)


# ======================================================
# OBTER TODAS AS LINHAS
# ======================================================

def get_records(nome_folha):

    worksheet = get_worksheet(nome_folha)

    return worksheet.get_all_records()


# ======================================================
# LIMPAR FOLHA
# ======================================================

def clear_sheet(nome_folha):

    worksheet = get_worksheet(nome_folha)

    worksheet.clear()
