# ======================================================
# CONFIGURAÇÃO DO SISTEMA (PRODUÇÃO)
# ======================================================
import os

class Config:

    # ==================================================
    # RESTAURANTE
    # ==================================================
    NOME_RESTAURANTE = "Dourados"
    SLOGAN = "Experiência Digital Moderna"

    LOGO = "/static/img/logo.png"
    BANNER = "/static/img/banner.jpg"

    # ==================================================
    # CORES
    # ==================================================
    COR_PRIMARIA = "#27ae60"
    COR_SECUNDARIA = "#111111"
    COR_DESTAQUE = "#f39c12"
    COR_FUNDO = "#101010"
    COR_CARD = "#FFFFFF"

    # ==================================================
    # CONTACTOS
    # ==================================================
    TELEFONE = "+258878605154"
    EMAIL = "firminosavel@gmail.com"
    DESENVOLVEDOR = "Firmino S. Savel"

    GOOGLE_MAPS = "https://www.google.com/maps/place/Dourados"

    # ==================================================
    # SISTEMA
    # ==================================================
    VERSAO = "2.0"
    EMPRESA = "Lume Solutions"
    COPYRIGHT = "© 2026 Todos os direitos reservados."

    # ==================================================
    # MOEDA
    # ==================================================
    MOEDA = "MZN"

    # ==================================================
    # IDIOMAS
    # ==================================================
    IDIOMAS = ["pt", "en"]

    # ==================================================
    # STATUS PEDIDOS
    # ==================================================
    STATUS_PEDIDO = [
        "Recebido",
        "Em Preparação",
        "Pronto",
        "Entregue",
        "Cancelado"
    ]

    # ==================================================
    # STATUS RESERVAS
    # ==================================================
    STATUS_RESERVA = [
        "Pendente",
        "Confirmada",
        "Concluída"
    ]

    # ==================================================
    # ADMIN
    # ==================================================
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    # ==================================================
    # AUTO REFRESH
    # ==================================================
    AUTO_REFRESH_ADMIN = 30
    AUTO_REFRESH_CLIENTE = 120  # 2 minutos como especificado no Master Project

    # ==================================================
    # GOOGLE SHEETS (NOMES DAS ABAS)
    # ==================================================
    SHEET_MENU = "Menu Digital"
    SHEET_ORDERS = "Pedidos"
    SHEET_RESERVATIONS = "Reservas"
    SHEET_CALLS = "Chamadas"
    SHEET_TABLES = "Mesas"
