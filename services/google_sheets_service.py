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
# CLIENTE GOOGLE
# ======================================================

def get_client():

    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not credentials_json:
        raise Exception(
            "GOOGLE_CREDENTIALS_JSON não encontrada nas Environment Variables."
        )

    credentials_dict = json.loads(credentials_json)

    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=SCOPES
    )

    return gspread.authorize(credentials)


# ======================================================
# ABRIR SHEET
# ======================================================

def open_sheet(sheet_name):

    client = get_client()

    return client.open(sheet_name)


# ======================================================
# LER UMA FOLHA
# ======================================================

def read_sheet(sheet_name, worksheet_name=None):

    spreadsheet = open_sheet(sheet_name)

    if worksheet_name:
        worksheet = spreadsheet.worksheet(worksheet_name)
    else:
        worksheet = spreadsheet.sheet1

    records = worksheet.get_all_records()

    return pd.DataFrame(records)


# ======================================================
# ESCREVER DATAFRAME
# ======================================================

def write_sheet(sheet_name, dataframe, worksheet_name=None):

    spreadsheet = open_sheet(sheet_name)

    if worksheet_name:
        worksheet = spreadsheet.worksheet(worksheet_name)
    else:
        worksheet = spreadsheet.sheet1

    worksheet.clear()

    worksheet.update(
        [dataframe.columns.values.tolist()] +
        dataframe.values.tolist()
    )


# ======================================================
# ADICIONAR LINHA
# ======================================================

def append_row(sheet_name, row, worksheet_name=None):

    spreadsheet = open_sheet(sheet_name)

    if worksheet_name:
        worksheet = spreadsheet.worksheet(worksheet_name)
    else:
        worksheet = spreadsheet.sheet1

    worksheet.append_row(row)
