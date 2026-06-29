# ======================================================
# CONFIGURAÇÕES GERAIS DO SISTEMA
# ======================================================

class Config:

    # ---------- RESTAURANTE ----------
    NOME_RESTAURANTE = "Dourados"
    SLOGAN = "Experiência Digital Moderna"

    LOGO = "/static/img/logo.png"
    BANNER = "/static/img/banner.jpg"

    # ---------- CORES ----------
    COR_PRIMARIA = "#27ae60"
    COR_SECUNDARIA = "#111111"
    COR_DESTAQUE = "#f39c12"
    COR_FUNDO = "#101010"
    COR_CARD = "#FFFFFF"

    # ---------- CONTACTOS ----------
    TELEFONE = "+258878605154"
    EMAIL = "firminosavel@gmail.com"
    DESENVOLVEDOR = "Firmino S. Savel"

    # ---------- LOCALIZAÇÃO ----------
    GOOGLE_MAPS = "https://www.google.com/maps/place/Dourados+Alojamentos,+E.I/@-25.4033605,32.8068776"

    # ---------- MOEDA ----------
    MOEDA = "MZN"

    # ---------- LOGIN ADMIN ----------
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

# ======================================================
# FICHEIROS
# ======================================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MENU_FILE = os.path.join(BASE_DIR, "data", "menu.xlsx")
ORDERS_FILE = os.path.join(BASE_DIR, "data", "pedidos.xlsx")
RESERVATIONS_FILE = os.path.join(BASE_DIR, "data", "reservas.xlsx")
CALLS_FILE = os.path.join(BASE_DIR, "data", "chamadas.xlsx")

    # ---------- STATUS PEDIDOS ----------
    STATUS_PEDIDO = [
        "Recebido",
        "Em Preparação",
        "Pronto",
        "Entregue"
    ]

    # ---------- STATUS RESERVAS ----------
    STATUS_RESERVA = [
        "Pendente",
        "Confirmada",
        "Concluída"
    ]

    # ---------- SISTEMA ----------
    VERSAO = "2.0"

    # ---------- COZINHA (TEMPO REAL) ----------
    COZINHA_REFRESH = 5  # segundos

    # ---------- DASHBOARD ----------
    MOSTRAR_ESTATS = True
