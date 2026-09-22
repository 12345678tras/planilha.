import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import Datavalidation
from openpyxl.formatting.rule import CellIsRule

# Bibliotecas novas para PDF e WhatsApp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# 1. Criação da Planilha do Sistema de Farmácia (openpyxl)
wb = openpyxl.Workbook()

# Aba 1: Painel de Controlo (Dashboard)
ws_dash = wb.active
ws_dash.title = "Painel de Controlo"
ws_dash.views.sheetView[0].showGridLines = True

# Aba 2: Estoque e Vendas
ws_inv = wb.create_sheet(title="Estoque e Vendas")
ws_inv.views.sheetView[0].showGridLines = True

# Aba 3: Fecho de Caixa (PIX, Dinheiro, Cartão)
ws_caixa = wb.create_sheet(title="Fecho de Caixa")
ws_caixa.views.sheetView[0].showGridLines = True

# Cores e Estilos Básicos
NAVY_HEADER = "0F172A"
LIGHT_BG = "F8FAFC"
WHITE = "FFFFFF"
GRAY_BORDER = "CBD5E1"
TEXT_DARK = "0F172A"

# --- FUNÇÕES DE SUPORTE PARA PDF E WHATSAPP ---

def gerar_relatorio_pdf(nome_arquivo="relatorio_farmacia.pdf"):
    """Gera um relatório básico em PDF com as informações do sistema."""
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.drawString(100, 750, "Sistema de Farmácia - Relatório Oficial")
    c.drawString(100, 730, "--------------------------------------------------------")
    c.drawString(100, 700, "Fecho de caixa e stock processados com sucesso.")
    c.save()
    print(f"[PDF] Relatório gerado com sucesso: {nome_arquivo}")

def enviar_mensagem_whatsapp(telefone, texto):
    """Prepara o envio de avisos ou resumos via WhatsApp."""
    # Aqui colocaria a URL da API de WhatsApp que usar no futuro (ex: Z-API, Twilio)
    url_api = "SUA_URL_DA_API_AQUI"
    payload = {
        "phone": telefone,
        "message": texto
    }
    # Exemplo de requisição (comentado para evitar erros sem a API configurada):
    # resposta = requests.post(url_api, json=payload)
    print(f"[WhatsApp] Mensagem simulada para o número {telefone}: {texto}")

# Execução de teste das novas funções ao iniciar o sistema
if __name__ == "__main__":
    print("A iniciar o Sistema de Farmácia...")
    
    # Salva a planilha de Excel como base
    nome_excel = "Sistema_Farmacia_Completo.xlsx"
    wb.save(nome_excel)
    print(f"[Excel] Planilha guardada com sucesso: {nome_excel}")
    
    # Testa a geração do PDF
    gerar_relatorio_pdf()
    
    # Testa a simulação de aviso por WhatsApp
    enviar_mensagem_whatsapp("5511999999999", "Sistema de farmácia atualizado e a funcionar!")
