# ======================================================
# HELPERS
# Funções auxiliares utilizadas por todo o sistema
# ======================================================

from datetime import datetime
import pytz
import pandas as pd
import os
import uuid


# ======================================================
# DATA/HORA MOÇAMBIQUE
# ======================================================
def hora_mocambique():

    tz = pytz.timezone("Africa/Maputo")
    agora = datetime.now(tz)

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    return f"{agora.day} {meses[agora.month]}, {agora.strftime('%H:%M')}"


# ======================================================
# LER EXCEL
# ======================================================
def load_excel(file_path):

    if os.path.exists(file_path):
        return pd.read_excel(file_path)

    return pd.DataFrame()


# ======================================================
# GUARDAR EXCEL
# ======================================================
def save_excel(file_path, dataframe):

    dataframe.to_excel(file_path, index=False)


# ======================================================
# GERAR UUID
# ======================================================
def gerar_id():

    return str(uuid.uuid4())


# ======================================================
# FORMATAR MOEDA
# ======================================================
def moeda(valor):

    try:
        return f"{float(valor):,.2f} MZN"
    except:
        return "0.00 MZN"


# ======================================================
# CRIAR PASTA CASO NÃO EXISTA
# ======================================================
def garantir_pasta(caminho):

    os.makedirs(caminho, exist_ok=True)


# ======================================================
# LOG SIMPLES
# ======================================================
def log(msg):

    print(f"[Restaurant App] {msg}")