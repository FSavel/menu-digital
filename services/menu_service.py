# ======================================================
# MENU SERVICE (GOOGLE SHEETS)
# ======================================================

import pandas as pd

from services.google_service import read_sheet

# ======================================================
# CONFIGURAÇÃO
# ======================================================

SHEET_NAME = "Menu Digital"


# ======================================================
# CARREGAR MENU
# ======================================================

def load_menu():

    try:

        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        # remover linhas completamente vazias
        df = df.dropna(how="all")

        # substituir NaN por vazio
        df = df.fillna("")

        return df.to_dict(orient="records")

    except Exception as e:

        print("Erro ao carregar menu:", e)

        return []


# ======================================================
# PESQUISAR PRODUTO
# ======================================================

def search_menu(texto):

    menu = load_menu()

    if not texto:
        return menu

    texto = texto.lower()

    resultado = []

    for item in menu:

        nome_pt = str(item.get("Produto_PT", "")).lower()
        nome_en = str(item.get("Produto_EN", "")).lower()
        descricao_pt = str(item.get("Descrição_PT", "")).lower()
        descricao_en = str(item.get("Descrição_EN", "")).lower()

        if (
            texto in nome_pt
            or texto in nome_en
            or texto in descricao_pt
            or texto in descricao_en
        ):
            resultado.append(item)

    return resultado


# ======================================================
# FILTRAR CATEGORIA
# ======================================================

def filter_category(categoria):

    menu = load_menu()

    if not categoria:
        return menu

    return [
        item
        for item in menu
        if item.get("Categoria") == categoria
    ]


# ======================================================
# OBTER PRODUTO
# ======================================================

def get_product(produto_id):

    menu = load_menu()

    for item in menu:

        if str(item.get("ID")) == str(produto_id):
            return item

    return None
