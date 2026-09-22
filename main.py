import streamlit as st
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

# Configuração da página
st.set_page_config(page_title="Sistema de Farmácia", page_icon="💊", layout="wide")

st.title("💊 Sistema de Farmácia - Gestão de Planilhas")
st.write("Painel de controlo e automação de fecho de caixa e stock.")

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

# Salva a planilha temporariamente para permitir o download
nome_excel = "Sistema_Farmacia_Completo.xlsx"
wb.save(nome_excel)

st.success("Planilha gerada com sucesso no sistema!")

# Botão para descarregar a planilha gerada diretamente na página
with open(nome_excel, "rb") as file:
    st.download_button(
        label="📥 Descarregar Planilha Excel",
        data=file,
        file_name=nome_excel,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
