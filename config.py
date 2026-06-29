# ======================================================
# CONFIGURAÇÃO DO SISTEMA (FASE 2)
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

    # ---------- SISTEMA ----------
    VERSAO = "2.0"
    EMPRESA = "Lume Solutions"
    COPYRIGHT = "© 2026 Todos os direitos reservados."

    # ---------- MOEDA ----------
    MOEDA = "MZN"

    # ---------- IDIOMAS ----------
    IDIOMAS = ["Português", "English"]

    # ---------- PEDIDOS ----------
    STATUS_PEDIDO = [
        "Recebido",
        "Em Preparação",
        "Pronto",
        "Entregue",
        "Cancelado"
    ]

    # ---------- RESERVAS ----------
    STATUS_RESERVA = [
        "Pendente",
        "Confirmada",
        "Concluída"
    ]

    # ---------- ADMIN (FASE 2) ----------
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"  # depois vamos securizar isto

    # ---------- FEATURES ----------
    MOSTRAR_TOTAL_DIA = True
    MOSTRAR_ESTATISTICAS = True

    # ---------- AUTO REFRESH ----------
    AUTO_REFRESH_ADMIN = 30
    AUTO_REFRESH_CLIENTE = 0

    # ---------- DADOS ----------
    MENU_FILE = "menu.xlsx"
    ORDERS_FILE = "pedidos.xlsx"
    RESERVATIONS_FILE = "reservas.xlsx"
    CALLS_FILE = "chamadas.xlsx"