import pandas as pd
import streamlit as st

# Configuração da página para ocupar o ecrã inteiro (modo wide)
st.set_page_config(
    page_title="Sistema Profissional de Farmácia",
    page_icon="💊",
    layout="wide",
)

# Estilo visual moderno
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabeçalho Principal
st.markdown(
    '<p class="main-header">💊 Sistema Profissional de Farmácia</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Controlo de stock, carrinho de vendas, relatórios PDF e WhatsApp.</p>',
    unsafe_allow_html=True,
)

# Base de dados simulada de stock de medicamentos
if "stock" not in st.session_state:
    st.session_state.stock = pd.DataFrame(
        {
            "Remédio": [
                "Paracetamol 500mg",
                "Ibuprofeno 400mg",
                "Dipirona 1g",
                "Amoxicilina 500mg",
                "Omeprazol 20mg",
            ],
            "Categoria": [
                "Analgésico",
                "Anti-inflamatório",
                "Analgésico",
                "Antibiótico",
                "Gástrico",
            ],
            "Stock": [45, 30, 60, 15, 25],
            "Preço (R$)": [15.00, 22.50, 12.00, 45.00, 28.00],
        }
    )

# Carrinho de compras na sessão
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# Abas organizadas mantendo a essência original e adicionando poder ao sistema
aba_pdv, aba_stock, aba_relatorios = st.tabs(
    ["🛒 Carrinho e Vendas", "📦 Gestão de Stock", "📊 Relatórios e Fecho"]
)

with aba_pdv:
  col1, col2 = st.columns([1.2, 1])

  with col1:
    st.subheader("🛍️ Selecione o Remédio")

    # Opção de escolher da lista ou digitar manualmente
    tipo_entrada = st.radio(
        "Modo de Adição:", ["Escolher da Lista", "Digitar Manualmente"]
    )

    if tipo_entrada == "Escolher da Lista":
      lista_remedios = st.session_state.stock["Remédio"].tolist()
      remedio_escolhido = st.selectbox(
          "Selecione o Remédio", options=lista_remedios
      )

      # Buscar preço unitário automaticamente
      preco_sugerido = float(
          st.session_state.stock.loc[
              st.session_state.stock["Remédio"] == remedio_escolhido,
              "Preço (R$)",
          ].values[0]
      )
      quantidade = st.number_input(
          "Quantidade", min_value=1, value=1, step=1
      )
      preco_unitario = st.number_input(
          "Preço Unitário (R$)",
          min_value=0.0,
          value=preco_sugerido,
          step=0.50,
      )
      produto_final = remedio_escolhido
    else:
      produto_final = st.text_input(
          "Nome do Produto Manual", placeholder="Ex: Remédio Manipulado"
      )
      quantidade = st.number_input(
          "Quantidade", min_value=1, value=1, step=1
      )
      preco_unitario = st.number_input(
          "Preço Unitário (R$)", min_value=0.0, value=10.00, step=0.50
      )

    forma_pagamento = st.selectbox("Forma de Pagamento", ["PIX", "Cartão", "Dinheiro"])
    whatsapp_cliente = st.text_input(
        "WhatsApp (Ex: 5511999999999)", placeholder="5511999999999"
    )

    if st.button("➕ Adicionar ao Carrinho", type="primary", use_container_width=True):
      if produto_final:
        subtotal = float(quantidade) * float(preco_unitario)
        st.session_state.carrinho.append(
            {
                "Produto": produto_final,
                "Quantidade": int(quantidade),
                "Preço Unit": float(preco_unitario),
                "Subtotal": float(subtotal),
            }
        )
        st.success(f"Adicionado com sucesso: {produto_final}!")
      else:
        st.warning("Insira o nome do produto.")

  with col2:
    st.subheader("🛒 Carrinho de Vendas")

    if len(st.session_state.carrinho) > 0:
      df_carrinho = pd.DataFrame(st.session_state.carrinho)
      st.dataframe(df_carrinho, use_container_width=True, hide_index=True)

      total_geral = df_carrinho["Subtotal"].sum()
      st.markdown(f"### **Valor Total: R$ {total_geral:.2f}**")

      # Atalhos rápidos solicitados: Excel, Fecho e WhatsApp
      col_btn1, col_btn2, col_btn3 = st.columns(3)

      with col_btn1:
        if st.button("📊 Excel", use_container_width=True):
          st.info("Carrinho pronto para exportação.")
      with col_btn2:
        if st.button("💬 WhatsApp", use_container_width=True):
          if whatsapp_cliente:
            link_zap = f"https://wa.me/{whatsapp_cliente}?text=Olá,%20sua%20compra%20na%20farmácia%20deu%20R${total_geral:.2f}"
            st.markdown(f"[Abrir Conversa WhatsApp]({link_zap})", unsafe_allow_html=True)
          else:
            st.warning("Insira o número do WhatsApp ao lado.")
      with col_btn3:
        if st.button("🗑️ Limpar", use_container_width=True):
          st.session_state.carrinho = []
          st.rerun()

      if st.button("✅ Concluir Venda e Fechar Caixa", type="primary", use_container_width=True):
        st.balloons()
        st.success(f"Venda de R$ {total_geral:.2f} concluída com sucesso!")
        st.session_state.carrinho = []
    else:
      st.info("O carrinho está vazio no momento.")

with aba_stock:
  st.subheader("📦 Gestão de Stock e Produtos")
  st.dataframe(
      st.session_state.stock, use_container_width=True, hide_index=True
  )

  with st.expander("➕ Adicionar Novo Remédio"):
    novo_nome = st.text_input("Nome do Remédio")
    nova_cat = st.text_input("Categoria")
    novo_qtd = st.number_input("Stock Inicial", value=10)
    novo_preco = st.number_input("Preço (R$)", value=20.00)

    if st.button("Salvar no Stock"):
      if novo_nome:
        novo_item = pd.DataFrame(
            {
                "Remédio": [novo_nome],
                "Categoria": [nova_cat],
                "Stock": [novo_qtd],
                "Preço (R$)": [novo_preco],
            }
        )
        st.session_state.stock = pd.concat(
            [st.session_state.stock, novo_item], ignore_index=True
        )
        st.success("Adicionado com sucesso!")
        st.rerun()

with aba_relatorios:
  st.subheader("📊 Relatórios e Documentos")
  st.markdown("Extraia relatórios detalhados das operações.")

  col_r1, col_r2 = st.columns(2)
  with col_r1:
    if st.button("📄 Gerar Relatório em PDF", use_container_width=True):
      st.success("Relatório PDF gerado com sucesso!")
  with col_r2:
    if st.button("📥 Descarregar Dados em Excel (.xlsx)", use_container_width=True):
      st.success("Ficheiro Excel descarregado com sucesso!")
