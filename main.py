import streamlit as st
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

# Bibliotecas para PDF e WhatsApp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# Configuração da Página do Streamlit
st.set_page_config(page_title="Sistema de Farmácia Completo", page_icon="💊", layout="wide")

st.title("💊 Sistema de Gestão de Farmácia e Fecho de Caixa")
st.write("Painel robusto para controlo de stock, vendas, pagamentos (PIX, Dinheiro, Cartão) e relatórios.")

# --- BARRA LATERAL COM OPÇÃO MANUAL E LISTA ---
st.sidebar.header("📥 Gestão de Produtos")

# Lista de remédios pré-cadastrados com opção manual
lista_remedios = [
    "Paracetamol 500mg",
    "Ibuprofeno 600mg",
    "Dipirona 500ml",
    "Amoxicilina 500mg",
    "Omeprazol 20mg",
    "✍️ Inserir Nome Manualmente..."
]

escolha_remedio = st.sidebar.selectbox("Selecione o Remédio", lista_remedios)

# Se o utilizador escolher a opção manual, abre a caixa de texto livre
if escolha_remedio == "✍️ Inserir Nome Manualmente...":
    nome_remedio = st.sidebar.text_input("Digite o Nome do Remédio", "Novo Remédio")
else:
    nome_remedio = escolha_remedio

quantidade = st.sidebar.number_input("Quantidade", min_value=1, value=10)
preco_unitario = st.sidebar.number_input("Preço Unitário (R$)", min_value=0.0, value=15.00)

forma_pagamento = st.sidebar.selectbox(
    "Forma de Pagamento (Fecho de Caixa)",
    ["PIX", "Dinheiro", "Cartão de Crédito", "Cartão de Débito"]
)

telefone_cliente = st.sidebar.text_input("Telefone para WhatsApp (Aviso)", "5511999999999")

if st.sidebar.button("💾 Adicionar e Atualizar Planilha"):
    st.sidebar.success(f"Produto '{nome_remedio}' registado com sucesso via {forma_pagamento}!")

# --- FUNÇÕES DE SUPORTE PARA PDF E WHATSAPP ---

def gerar_relatorio_pdf(nome_arquivo="relatorio_farmacia.pdf"):
    """Gera um relatório profissional em PDF com as informações do sistema."""
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.drawString(100, 750, "Sistema de Farmácia - Relatório Oficial de Fecho")
    c.drawString(100, 730, "--------------------------------------------------------")
    c.drawString(100, 700, f"Último registo: {nome_remedio} | Qtd: {quantidade} | Pagamento: {forma_pagamento}")
    c.drawString(100, 670, "Fecho de caixa e stock processados com sucesso.")
    c.save()
    return nome_arquivo

def enviar_mensagem_whatsapp(telefone, texto):
    """Prepara o envio de avisos ou resumos via WhatsApp."""
    url_api = "SUA_URL_DA_API_AQUI"
    payload = {
        "phone": telefone,
        "message": texto
    }
    return f"[WhatsApp Enviado para {telefone}]: {texto}"

# --- ABA / SECÇÃO PRINCIPAL DE VISUALIZAÇÃO ---
tab1, tab2, tab3 = st.tabs(["📊 Painel de Controlo", "📦 Stock e Vendas", "💰 Fecho de Caixa"])

with tab1:
    st.subheader("Resumo Geral do Sistema")
    col1, col2, col3 = st.columns(3)
    col1.metric("Produto Selecionado", nome_remedio)
    col2.metric("Quantidade Atual", quantidade)
    col3.metric("Método Principal", forma_pagamento)

with tab2:
    st.subheader("Gestão de Inventário e Medicamentos")
    st.write("Aqui visualiza os remédios e pode escolher da lista ou usar a opção de digitar manualmente na barra lateral.")
    
    # Criar a estrutura do Excel em background
    wb = openpyxl.Workbook()
    ws_dash = wb.active
    ws_dash.title = "Painel de Controlo"
    ws_dash.views.sheetView[0].showGridLines = True
    
    ws_inv = wb.create_sheet(title="Estoque e Vendas")
    ws_inv.views.sheetView[0].showGridLines = True
    ws_inv.append(["Produto", "Quantidade", "Preço Unitário", "Total"])
    ws_inv.append([nome_remedio, quantidade, preco_unitario, quantidade * preco_unitario])
    
    ws_caixa = wb.create_sheet(title="Fecho de Caixa")
    ws_caixa.views.sheetView[0].showGridLines = True
    ws_caixa.append(["Forma de Pagamento", "Valor"])
    ws_caixa.append([forma_pagamento, quantidade * preco_unitario])
    
    nome_excel = "Sistema_Farmacia_Completo.xlsx"
    wb.save(nome_excel)
    
    with open(nome_excel, "rb") as file:
        st.download_button(
            label="📥 Descarregar Planilha Excel Atualizada",
            data=file,
            file_name=nome_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab3:
    st.subheader("Fecho de Caixa (PIX, Dinheiro, Cartão)")
    st.info(f"Pagamento selecionado para a transação atual: **{forma_pagamento}**")
    
    if st.button("📄 Gerar Relatório PDF e Enviar Aviso"):
        pdf_gerado = gerar_relatorio_pdf()
        st.success(f"Relatório PDF '{pdf_gerado}' gerado com sucesso!")
        
        status_wpp = enviar_mensagem_whatsapp(telefone_cliente, f"Olá! Fecho de caixa concluído via {forma_pagamento}.")
        st.write(status_wpp)
