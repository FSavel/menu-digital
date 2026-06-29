# ======================================================
# MENU SERVICE
# Responsável pela leitura do menu
# ======================================================

import pandas as pd
import os


# ======================================================
# CARREGAR MENU
# ======================================================
def load_menu(file_path):

    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)

    return df.to_dict(orient="records")


# ======================================================
# PESQUISAR PRODUTO
# ======================================================
def search_menu(file_path, texto):

    menu = load_menu(file_path)

    if not texto:
        return menu

    texto = texto.lower()

    return [
        produto
        for produto in menu
        if texto in str(produto.get("nome", "")).lower()
    ]


# ======================================================
# FILTRAR CATEGORIA
# ======================================================
def filter_category(file_path, categoria):

    menu = load_menu(file_path)

    if not categoria:
        return menu

    return [
        produto
        for produto in menu
        if produto.get("categoria") == categoria
    ]


# ======================================================
# PRODUTO POR ID
# ======================================================
def get_product(file_path, product_id):

    menu = load_menu(file_path)

    for produto in menu:

        if str(produto.get("id")) == str(product_id):
            return produto

    return None