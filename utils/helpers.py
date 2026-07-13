# ======================================================
# HELPERS
# Funções auxiliares utilizadas por todo o sistema
# ======================================================
from datetime import datetime
import pytz
import uuid

# ======================================================
# DATA/HORA MOÇAMBIQUE
# ======================================================
def hora_mocambique():
    try:
        tz = pytz.timezone("Africa/Maputo")
        agora = datetime.now(tz)

        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }

        return f"{agora.day} {meses[agora.month]}, {agora.strftime('%H:%M')}"
    except Exception as e:
        print("[Helpers] Erro ao obter fuso horário:", e)
        return datetime.now().strftime("%d/%m/%Y, %H:%M")


# ======================================================
# GERAR ID ÚNICO CURTO (Focado em Produção SaaS)
# ======================================================
def gerar_id():
    # Cria uma chave limpa, curta e profissional de 6 caracteres em maiúsculas (ex: X9A8F2)
    # Muito mais legível para a cozinha e para o dashboard do que um UUID completo.
    return uuid.uuid4().hex[:6].upper()


# ======================================================
# FORMATAR MOEDA (METICAIS - MT / MZN)
# ======================================================
def moeda(valor, simbolo="MT"):
    try:
        if valor is None:
            return f"0.00 {simbolo}"
        return f"{float(valor):,.2f} {simbolo}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return f"0.00 {simbolo}"


# ======================================================
# LOG SIMPLES
# ======================================================
def log(msg):
    print(f"[Dourados SaaS] {msg}")
