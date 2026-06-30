# ======================================================
# CONFIG SERVICE
# Lê as configurações do restaurante no Google Sheets
# ======================================================

from services.google_service import read_sheet

SHEET_NAME = "Config"


def load_config():

    try:

        df = read_sheet(SHEET_NAME)

        if df.empty:
            return {}

        config = {}

        for _, row in df.iterrows():

            chave = str(row.get("Chave", "")).strip()
            valor = str(row.get("Valor", "")).strip()

            if chave:
                config[chave] = valor

        return config

    except Exception as e:

        print("Erro ao carregar Config:", e)
        return {}