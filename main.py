import streamlit as st
import openpyxl
from openpyxl.worksheet.views import SheetView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# 1. Configuração da Página
st.set_page_config(page_title="Sistema de Farmácia", page_icon="💊", layout="wide")

st.title("💊 Sistema Profissional de Gestão de Farmácia")
st.markdown("Controlo de stock, carrinho de vendas, relatórios PDF e WhatsApp.")
st.divider()

# 2. Inicialização do Estado
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "forma_pagamento" not in st.session_state:
    st.session_state.forma_pagamento = "PIX"

# 3. Barra Lateral (Entrada)
st.sidebar.header("📥 Gestão de Produtos")

lista_remedios = [
    "Paracetamol 500mg",
    "Ibuprofeno 600mg",
    "Dipirona 500ml",
    "Amoxicilina 500mg",
    "Omeprazol 20mg",
    "✍️ Inserir Manualmente..."
]

escolha = st.sidebar.selectbox("Selecione o Remédio", lista_remedios)

if escolha == "✍️ Inserir Manualmente...":
    nome_remedio = st.sidebar.text_input("Nome do Remédio", "Novo Remédio")
else:
    nome_remedio = escolha

quantidade = st.sidebar.number_input("Quantidade", min_value=1, value=1)
preco_unitario = st.sidebar.number_input("Preço Unitário (R$)", min_value=0.0, value=15.00)

st.session_state.forma_pagamento = st.sidebar.selectbox(
    "Forma de Pagamento",
    ["PIX", "Dinheiro", "Cartão de Crédito", "Cartão de Débito"]
)

telefone_cliente = st.sidebar.text_input("WhatsApp (Ex: 5511999999999)", "5511999999999")

st.sidebar.divider()

if st.sidebar.button("➕ Adicionar ao Carrinho", type="primary", use_container_width=True):
    subtotal = quantidade * preco_unitario
    st.session_state.carrinho.append({
        "produto": nome_remedio,
        "quantidade": quantidade,
        "preco": preco_unitario,
        "subtotal": subtotal,
        "pagamento": st.session_state.forma_pagamento
    })
    st.sidebar.success(f"Adicionado: {nome_remedio}")

if st.sidebar.button("🗑️ Limpar Carrinho", use_container_width=True):
    st.session_state.carrinho = []
    st.sidebar.warning("Carrinho limpo.")

# 4. Função PDF
def gerar_relatorio_pdf(nome_arquivo="relatorio_fecho_caixa.pdf"):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.drawString(100, 750, "Sistema de Farmácia - Relatório de Fecho")
    c.drawString(100, 730, "-" * 55)
    
    y = 700
    total_geral = 0
    for item in st.session_state.carrinho:
        linha = f"- {item['produto']} | Qtd: {item['quantidade']} | Subtotal: R$ {item['subtotal']:.2f} ({item['pagamento']})"
        c.drawString(100, y, linha)
        total_geral += item['subtotal']
        y -= 25
        if y < 100:
            c.showPage()
            y = 750
            
    c.drawString(100, y - 20, f"TOTAL GERAL: R$ {total_geral:.2f}")
    c.save()
    return nome_arquivo

# 5. Abas Principais
tab1, tab2, tab3 = st.tabs(["📊 Carrinho", "📦 Excel", "💰 Fecho e WhatsApp"])

with tab1:
    st.subheader("Carrinho de Vendas")
    if st.session_state.carrinho:
        total_acumulado = 0
        for i, item in enumerate(st.session_state.carrinho):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            col1.write(f"**{i+1}. {item['produto']}**")
            col2.write(f"Qtd: {item['quantidade']}")
            col3.write(f"R$ {item['subtotal']:.2f}")
            col4.write(f"[{item['pagamento']}]")
            total_acumulado += item['subtotal']
        st.divider()
        st.markdown(f"### **Valor Total: R$ {total_acumulado:.2f}**")
    else:
        st.info("O carrinho está vazio.")

with tab2:
    st.subheader("Gerador de Excel")
    if st.session_state.carrinho:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Vendas"
        if ws.views.sheetView:
            ws.views.sheetView[0].showGridLines = True
        else:
            ws.views.sheetView.append(SheetView(showGridLines=True))
            
        ws.append(["Produto", "Quantidade", "Preço Unitário", "Subtotal", "Pagamento"])
        for item in st.session_state.carrinho:
            ws.append([item["produto"], item["quantidade"], item["preco"], item["subtotal"], item["pagamento"]])
        
        nome_excel = "Sistema_Farmacia.xlsx"
        wb.save(nome_excel)
        
        with open(nome_excel, "rb") as file:
            st.download_button(label="📥 Baixar Planilha Excel", data=file, file_name=nome_excel, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    else:
        st.warning("Adicione produtos para gerar a planilha.")

with tab3:
    st.subheader("Fecho, PDF e WhatsApp")
    if st.session_state.carrinho:
        col_pdf, col_wpp = st.columns(2)
        with col_pdf:
            if st.button("Gerar PDF de Fecho", use_container_width=True):
                pdf_gerado = gerar_relatorio_pdf()
                st.success("PDF gerado!")
                with open(pdf_gerado, "rb") as pdf_file:
                    st.download_button(label="📥 Baixar PDF", data=pdf_file, file_name=pdf_gerado, mime="application/pdf", use_container_width=True)
        with col_wpp:
            total_venda = sum(item['subtotal'] for item in st.session_state.carrinho)
            texto_wpp = f"Fecho de caixa realizado. Total: R$ {total_venda:.2f} via {st.session_state.forma_pagamento}."
            link_whatsapp = f"https://wa.me/{telefone_cliente}?text={requests.utils.quote(texto_wpp)}"
            st.markdown(f'<a href="{link_whatsapp}" target="_blank"><button style="background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer; width:100%;">🚀 Enviar no WhatsApp</button></a>', unsafe_allow_html=True)
    else:
        st.warning("Adicione produtos ao carrinho.")
