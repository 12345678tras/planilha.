import pandas as pd
import streamlit as st

# Configuração da página para ocupar o ecrã inteiro (modo wide)
st.set_page_config(
    page_title="Sistema Profissional de Farmácia",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo visual moderno com CSS personalizado
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
    .stMetric {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    '<p class="sub-header">Controlo de stock, frente de caixa (PDV), carrinho, fecho de caixa e relatórios avançados.</p>',
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

# Abas de Navegação Super Organizadas
aba_pdv, aba_stock, aba_clientes, aba_relatorios = st.tabs(
    [
        "🛒 Frente de Caixa (PDV)",
        "📦 Gestão de Stock",
        "👥 Clientes",
        "📊 Relatórios e Fecho",
    ]
)

with aba_pdv:
  col1, col2 = st.columns([1.2, 1])

  with col1:
    st.subheader("🛍️ Registar Venda")

    # Opção de seleção ou digitação manual
    modo_produto = st.radio(
        "Modo de entrada do produto:",
        ["Selecionar da Lista", "Digitar Manualmente"],
        horizontal=True,
    )

    if modo_produto == "Selecionar da Lista":
      lista_remedios = st.session_state.stock["Remédio"].tolist()
      remedio_escolhido = st.selectbox(
          "Selecione o Remédio", options=lista_remedios
      )

      # Buscar preço unitário automaticamente do stock
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
          format="%.2f",
      )
      produto_final = remedio_escolhido

    else:
      st.info(
          "Modo manual ativado: insira livremente o produto que não está no"
          " catálogo."
      )
      produto_final = st.text_input(
          "Nome do Produto / Remédio", placeholder="Ex: Vitamina C Efervescente"
      )
      quantidade = st.number_input(
          "Quantidade", min_value=1, value=1, step=1
      )
      preco_unitario = st.number_input(
          "Preço Unitário (R$)", min_value=0.0, value=10.00, step=0.50
      )

    forma_pagamento = st.selectbox(
        "Forma de Pagamento", ["PIX", "Cartão de Crédito", "Dinheiro", "Boleto"]
    )
    whatsapp_cliente = st.text_input(
        "WhatsApp do Cliente (Opcional)", placeholder="Ex: 5511999999999"
    )

    if st.button("➕ Adicionar ao Carrinho", type="primary", use_container_width=True):
      if produto_final:
        subtotal = quantidade * preco_unitario
        st.session_state.carrinho.append(
            {
                "Produto": produto_final,
                "Qtd": quantidade,
                "Preço Unit": preco_unitario,
                "Subtotal": subtotal,
            }
        )
        st.success(
            f"Adicionado: {quantidade}x {produto_final} (R$ {subtotal:.2f})"
        )
      else:
        st.warning("Por favor, informe o nome do produto.")

  with col2:
    st.subheader("🛒 Carrinho de Vendas Atual")

    if len(st.session_state.carrinho) > 0:
      df_carrinho = pd.DataFrame(st.session_state.carrinho)
      st.dataframe(df_carrinho, use_container_width=True, hide_index=True)

      total_geral = df_carrinho["Subtotal"].sum()
      st.markdown(f"### **Valor Total: R$ {total_geral:.2f}**")

      col_a, col_b = st.columns(2)
      with col_a:
        if st.button(
            "🗑️ Limpar Carrinho", use_container_width=True, type="secondary"
        ):
          st.session_state.carrinho = []
          st.rerun()
      with col_b:
        if st.button(
            "✅ Finalizar Venda", use_container_width=True, type="primary"
        ):
          st.balloons()
          st.success(
              f"Venda no valor de R$ {total_geral:.2f} finalizada com sucesso via"
              f" {forma_pagamento}!"
          )
          st.session_state.carrinho = []
    else:
      st.info(
          "O carrinho está vazio. Adicione produtos ao lado para montar a"
          " venda."
      )

with aba_stock:
  st.subheader("📦 Gestão e Controlo de Stock")
  st.markdown("Consulte os produtos disponíveis e adicione novos itens ao sistema.")

  # Tabela de Stock Atual
  st.dataframe(
      st.session_state.stock, use_container_width=True, hide_index=True
  )

  with st.expander("➕ Adicionar Novo Remédio ao Catálogo"):
    with st.form("form_novo_produto"):
      novo_nome = st.text_input("Nome do Remédio / Produto")
      nova_categoria = st.text_input("Categoria (Ex: Analgésico, Vitamina)")
      novo_stock = st.number_input("Quantidade em Stock", min_value=0, value=10)
      novo_preco = st.number_input(
          "Preço de Venda (R$)", min_value=0.0, value=20.00
      )

      submitted = st.form_submit_button("Guardar no Catálogo")
      if submitted and novo_nome:
        novo_df = pd.DataFrame(
            {
                "Remédio": [novo_nome],
                "Categoria": [nova_categoria],
                "Stock": [novo_stock],
                "Preço (R$)": [novo_preco],
            }
        )
        st.session_state.stock = pd.concat(
            [st.session_state.stock, novo_df], ignore_index=True
        )
        st.success(f"Produto '{novo_nome}' adicionado com sucesso!")
        st.rerun()

with aba_clientes:
  st.subheader("👥 Registo de Clientes")
  st.markdown("Consulte a base de clientes frequentes da farmácia.")

  df_clientes = pd.DataFrame(
      {
          "Nome": ["Ana Souza", "Carlos Silva", "Mariana Oliveira"],
          "Telefone": ["(11) 98888-1111", "(11) 97777-2222", "(11) 96666-3333"],
          "Última Compra": ["2026-09-20", "2026-09-21", "2026-09-22"],
          "Pontos Fidelidade": [120, 45, 90],
      }
  )
  st.dataframe(df_clientes, use_container_width=True, hide_index=True)

with aba_relatorios:
  st.subheader("📊 Relatórios e Fecho de Caixa")
  st.markdown("Visualize o resumo financeiro e exporte relatórios.")

  col_m1, col_m2, col_m3 = st.columns(3)
  with col_m1:
    st.metric(
        label="Vendas Realizadas Hoje", value="R$ 1.450,00", delta="+12%"
    )
  with col_m2:
    st.metric(label="Atendimentos", value="38 clientes", delta="+5")
  with col_m3:
    st.metric(label="Ticket Médio", value="R$ 38,15", delta="Estável")

  st.divider()

  # Botões de exportação simulados para Excel e PDF
  col_exp1, col_exp2 = st.columns(2)
  with col_exp1:
    if st.button("📥 Exportar Relatório em Excel (.xlsx)", use_container_width=True):
      st.success("Relatório exportado para Excel com sucesso!")
  with col_exp2:
    if st.button("📄 Gerar Relatório em PDF", use_container_width=True):
      st.success("Relatório gerado em PDF com sucesso!")
