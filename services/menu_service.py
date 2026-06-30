# ======================================================
# MENU SERVICE (GOOGLE SHEETS ONLY)
# ======================================================

import pandas as pd
from services.google_service import read_sheet

# ======================================================
# CONFIGURAÇÃO
# ======================================================

SHEET_NAME = "Menu Digital"

# ======================================================
# CARREGAR MENU (PRINCIPAL)
# ======================================================

def load_menu():

    try:
        df = read_sheet(SHEET_NAME)

        if df.empty:
            return []

        # limpar dados
        df = df.dropna(how="all")
        df = df.fillna("")

        return df.to_dict(orient="records")

    except Exception as e:
        print("[Menu Service] Erro ao carregar menu:", e)
        return []


# ======================================================
# PESQUISA DE PRODUTOS
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
        desc_pt = str(item.get("Descrição_PT", "")).lower()
        desc_en = str(item.get("Descrição_EN", "")).lower()

        if (
            texto in nome_pt
            or texto in nome_en
            or texto in desc_pt
            or texto in desc_en
        ):
            resultado.append(item)

    return resultado


# ======================================================
# FILTRAR POR CATEGORIA
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
# OBTER PRODUTO POR ID
# ======================================================

def get_product(produto_id):

    menu = load_menu()

    for item in menu:
        if str(item.get("ID")) == str(produto_id):
            return item

    return None
