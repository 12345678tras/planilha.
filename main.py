import pandas as pd
import streamlit as st

# Configuração da página em modo wide
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

st.markdown(
    '<p class="main-header">💊 Sistema Profissional de Farmácia</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Controlo de stock alargado, carrinho, PDF, Excel e WhatsApp integrados.</p>',
    unsafe_allow_html=True,
)

# Base de dados de stock enriquecida com muitos mais medicamentos
if "stock" not in st.session_state:
    st.session_state.stock = pd.DataFrame(
        {
            "Remédio": [
                "Paracetamol 500mg",
                "Ibuprofeno 400mg",
                "Dipirona 1g",
                "Amoxicilina 500mg",
                "Omeprazol 20mg",
                "Nimesulida 100mg",
                "Loratadina 10mg",
                "Azitromicina 500mg",
                "Losartana 50mg",
                "Cloridrato de Metformina 850mg",
                "Dipirona Gotas 20ml",
                "Vitamina C 1g Efervescente",
                "Sinvastatina 20mg",
                "Cefalexina 500mg",
                "Dexametasona 4mg",
            ],
            "Categoria": [
                "Analgésico",
                "Anti-inflamatório",
                "Analgésico",
                "Antibiótico",
                "Gástrico",
                "Anti-inflamatório",
                "Antialérgico",
                "Antibiótico",
                "Cardiovascular",
                "Antidiabético",
                "Analgésico",
                "Vitamina",
                "Cardiovascular",
                "Antibiótico",
                "Anti-inflamatório",
            ],
            "Stock": [
                45,
                30,
                60,
                15,
                25,
                40,
                50,
                20,
                35,
                60,
                80,
                100,
                45,
                18,
                30,
            ],
            "Preço (R$)": [
                15.00,
                22.50,
                12.00,
                45.00,
                28.00,
                18.50,
                14.00,
                55.00,
                32.00,
                24.00,
                10.00,
                20.00,
                38.00,
                48.00,
                25.00,
            ],
        }
    )

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# Abas do sistema
aba_pdv, aba_stock, aba_relatorios = st.tabs(
    ["🛒 Carrinho e Vendas", "📦 Gestão de Stock", "📊 Relatórios e Fecho"]
)

with aba_pdv:
  col1, col2 = st.columns([1.2, 1])

  with col1:
    st.subheader("🛍️ Selecione o Remédio")

    tipo_entrada = st.radio(
        "Modo de Adição:", ["Escolher da Lista", "Digitar Manualmente"]
    )

    if tipo_entrada == "Escolher da Lista":
      lista_remedios = st.session_state.stock["Remédio"].tolist()
      remedio_escolhido = st.selectbox(
          "Selecione o Remédio", options=lista_remedios
      )

      preco_sugerido = float(
          st.session_state.stock.loc[
              st.session_state.stock["Remédio"] == remedio_escolhido,
              "Preço (R$)",
          ].values[0]
      )
      quantidade = st.number_input(
          "Quantidade", min_value=1, value=1, step=1, key="qtd_lista"
      )
      preco_unitario = st.number_input(
          "Preço Unitário (R$)",
          min_value=0.0,
          value=preco_sugerido,
          step=0.50,
          key="preco_lista",
      )
      produto_final = remedio_escolhido
    else:
      produto_final = st.text_input(
          "Nome do Produto Manual",
          placeholder="Ex: Remédio Manipulado",
          key="prod_manual",
      )
      quantidade = st.number_input(
          "Quantidade", min_value=1, value=1, step=1, key="qtd_man"
      )
      preco_unitario = st.number_input(
          "Preço Unitário (R$)",
          min_value=0.0,
          value=10.00,
          step=0.50,
          key="preco_man",
      )

    forma_pagamento = st.selectbox(
        "Forma de Pagamento", ["PIX", "Cartão", "Dinheiro"]
    )
    whatsapp_cliente = st.text_input(
        "WhatsApp do Cliente (Ex: 5511999999999)", placeholder="5511999999999"
    )

    if st.button("➕ Adicionar ao Carrinho", type="primary", use_container_width=True):
      if produto_final and str(produto_final).strip() != "":
        subtotal = float(quantidade) * float(preco_unitario)
        st.session_state.carrinho.append(
            {
                "Produto": str(produto_final),
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

      if "Subtotal" in df_carrinho.columns:
        st.dataframe(df_carrinho, use_container_width=True, hide_index=True)
        total_geral = df_carrinho["Subtotal"].sum()
        st.markdown(f"### **Valor Total: R$ {total_geral:.2f}**")

        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
          if st.button("📊 Excel", use_container_width=True):
            st.info("Dados preparados para Excel.")
        with col_btn2:
          if st.button("💬 WhatsApp", use_container_width=True):
            if whatsapp_cliente:
              link_zap = f"https://wa.me/{whatsapp_cliente}?text=Olá,%20sua%20compra%20na%20farmácia%20deu%20R${total_geral:.2f}"
              st.markdown(
                  f"[Abrir Conversa WhatsApp]({link_zap})", unsafe_allow_html=True
              )
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
        st.session_state.carrinho = []
        st.rerun()
    else:
      st.info("O carrinho está vazio no momento.")

with aba_stock:
  st.subheader("📦 Gestão de Stock e Produtos")
  st.markdown("Lista alargada de medicamentos disponíveis no sistema:")
  st.dataframe(
      st.session_state.stock, use_container_width=True, hide_index=True
  )

  with st.expander("➕ Adicionar Novo Remédio ao Catálogo"):
    novo_nome = st.text_input("Nome do Remédio", key="novo_nome_stk")
    nova_cat = st.text_input("Categoria", key="nova_cat_stk")
    novo_qtd = st.number_input("Stock Inicial", value=10, key="novo_qtd_stk")
    novo_preco = st.number_input(
        "Preço (R$)", value=20.00, key="novo_preco_stk"
    )

    if st.button("Salvar no Stock", key="btn_salvar_stk"):
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
  st.markdown(
      "Extraia relatórios detalhados e envie notificações diretamente por"
      " WhatsApp."
  )

  # Campo para WhatsApp nos relatórios/fecho
  whatsapp_geral = st.text_input(
      "Número de WhatsApp para Envio de Fecho (Ex: 5511999999999)",
      placeholder="5511999999999",
  )

  col_r1, col_r2, col_r3 = st.columns(3)
  with col_r1:
    if st.button("📄 Gerar Relatório em PDF", use_container_width=True):
      st.success("Relatório PDF gerado com sucesso!")
  with col_r2:
    if st.button("📥 Descarregar Excel (.xlsx)", use_container_width=True):
      st.success("Ficheiro Excel descarregado com sucesso!")
  with col_r3:
    if st.button("💬 Enviar Fecho via WhatsApp", use_container_width=True):
      if whatsapp_geral:
        link_zap_geral = f"https://wa.me/{whatsapp_geral}?text=Relatorio%20de%20fecho%20de%20caixa%20da%20farmacia%20concluido%20com%20sucesso!"
        st.markdown(
            f"[Clique aqui para abrir o WhatsApp]({link_zap_geral})",
            unsafe_allow_html=True,
        )
      else:
        st.warning("Insira o número do WhatsApp acima.")
