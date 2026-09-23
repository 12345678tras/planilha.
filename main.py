import io
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
    '<p class="sub-header">Catálogo comercial com 500 produtos, PDV, PDF, Excel e WhatsApp integrados.</p>',
    unsafe_allow_html=True,
)

# Base de dados de stock comercial com 500 itens essenciais de farmácia
if "stock" not in st.session_state:
  nomes_base = [
      "Paracetamol",
      "Dipirona",
      "Ibuprofeno",
      "Nimesulida",
      "Amoxicilina",
      "Azitromicina",
      "Omeprazol",
      "Losartana",
      "Metformina",
      "Sinvastatina",
      "Loratadina",
      "Cefalexina",
      "Dexametasona",
      "Vitamina C",
      "Dipirona Gotas",
      "Paracetamol Gotas",
      "Ibuprofeno Gotas",
      "Buscopan",
      "Dorflex",
      "Neosoro",
      "Vick VapoRub",
      "Xarope Xantinon",
      "Esperson",
      "Aspirina",
      "Cataflan",
      "Alivium",
      "Novalgina",
      "Tylenol",
      "Cimegripe",
      "Benegrip",
      "Resfenol",
      "Engov",
      "Sonrisal",
      "Eno",
      "Estomazil",
      "Alka-Seltzer",
      "Luftal",
      "Imosec",
      "Fenergan",
      "Polaramine",
      "Allegra",
      "Zyx",
      "Desalex",
      "Rinosoro",
      "Sorine",
      "Neotric",
      "Nebacetin",
      "Bepantol",
      "Glicerina Supositório",
      "Leite de Magnésia",
  ]
  categorias_base = [
      "Analgésico",
      "Analgésico",
      "Anti-inflamatório",
      "Anti-inflamatório",
      "Antibiótico",
      "Antibiótico",
      "Gástrico",
      "Cardiovascular",
      "Antidiabético",
      "Cardiovascular",
      "Antialérgico",
      "Antibiótico",
      "Anti-inflamatório",
      "Vitamina",
      "Analgésico",
      "Analgésico",
      "Anti-inflamatório",
      "Espasmódico",
      "Relaxante Muscular",
      "Descongestionante",
      "Gripes e Cuidado",
      "Digestivo",
      "Dermatológico",
      "Analgésico",
      "Anti-inflamatório",
      "Anti-inflamatório",
      "Analgésico",
      "Analgésico",
      "Gripe",
      "Gripe",
      "Gripe",
      "Ressaca",
      "Estomacal",
      "Estomacal",
      "Estomacal",
      "Estomacal",
      "Gases",
      "Antidiarreico",
      "Antialérgico",
      "Antialérgico",
      "Antialérgico",
      "Antialérgico",
      "Antialérgico",
      "Nasal",
      "Nasal",
      "Oftalmológico",
      "Dermatológico",
      "Dermatológico",
      "Laxante",
      "Estomacal",
  ]

  lista_produtos = []
  lista_categorias = []
  lista_stock = []
  lista_precos = []

  dosagens = ["200mg", "400mg", "500mg", "1g", "50ml", "100ml", "30 cpr", "60 cpr"]

  contador = 1
  while len(lista_produtos) < 500:
    base_idx = (contador - 1) % len(nomes_base)
    nome_original = nomes_base[base_idx]
    cat_original = categorias_base[base_idx]

    if contador <= len(nomes_base):
      produto_nome = f"{nome_original} Padrão"
    else:
      dosagem_escolhida = dosagens[(contador * 3) % len(dosagens)]
      produto_nome = f"{nome_original} {dosagem_escolhida} (L{contador})"

    lista_produtos.append(produto_nome)
    lista_categorias.append(cat_original)
    lista_stock.append(15 + (contador * 7) % 85)
    lista_precos.append(round(8.50 + ((contador * 3.25) % 85.00), 2))
    contador += 1

  st.session_state.stock = pd.DataFrame({
      "Remédio": lista_produtos,
      "Categoria": lista_categorias,
      "Stock": lista_stock,
      "Preço (R$)": lista_precos,
  })

if "carrinho" not in st.session_state:
  st.session_state.carrinho = []

if "venda_concluida" not in st.session_state:
  st.session_state.venda_concluida = False
  st.session_state.ultimo_total = 0.0
  st.session_state.itens_ultima_venda = []

# Abas do sistema
aba_pdv, aba_stock, aba_relatorios = st.tabs(
    ["🛒 Carrinho e Vendas", "📦 Gestão de Stock (500+)", "📊 Relatórios e Fecho"]
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
          "Selecione o Remédio (500+ opções)", options=lista_remedios
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
          placeholder="Ex: Produto Especial Balcão",
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
        "WhatsApp do Cliente (Opcional - Ex: 5511999999999)",
        placeholder="5511999999999",
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
          # Botão Excel direto no carrinho
          buffer_excel = io.BytesIO()
          with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
            df_carrinho.to_excel(writer, index=False, sheet_name="Carrinho")
          buffer_excel.seek(0)

          st.download_button(
              label="📊 Excel",
              data=buffer_excel,
              file_name="carrinho_venda.xlsx",
              mime=(
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              ),
              use_container_width=True,
          )

        with col_btn2:
          if st.button("💬 WhatsApp", use_container_width=True):
            if whatsapp_cliente.strip():
              link_zap = f"https://wa.me/{whatsapp_cliente}?text=Olá,%20sua%20compra%20na%20farmácia%20deu%20R${total_geral:.2f}"
            else:
              link_zap = f"https://wa.me/?text=Olá,%20o%20total%20da%20compra%20na%20farmácia%20é%20R${total_geral:.2f}"

            st.markdown(
                f"[🔗 Abrir WhatsApp]({link_zap})", unsafe_allow_html=True
            )
        with col_btn3:
          if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.carrinho = []
            st.session_state.venda_concluida = False
            st.rerun()

        if st.button("✅ Concluir Venda e Fechar Caixa", type="primary", use_container_width=True):
          st.balloons()
          st.session_state.venda_concluida = True
          st.session_state.ultimo_total = total_geral
          st.session_state.itens_ultima_venda = st.session_state.carrinho.copy()
          st.session_state.carrinho = []
          st.rerun()
      else:
        st.session_state.carrinho = []
        st.rerun()
    else:
      if st.session_state.venda_concluida:
        st.success(
            f"✅ Venda de R$ {st.session_state.ultimo_total:.2f} concluída com"
            " sucesso!"
        )
        st.markdown("### Ações Pós-Venda:")

        col_pos1, col_pos2, col_pos3 = st.columns(3)
        with col_pos1:
          # Geração do Comprovativo em Texto formatado como relatório descarregável
          texto_recibo = f"""========================================
       COMPROVATIVO DE VENDA - FARMÁCIA
========================================
Valor Total: R$ {st.session_state.ultimo_total:.2f}
Forma de Pagamento: {forma_pagamento}
----------------------------------------
Itens da Venda:
"""
          for item in st.session_state.itens_ultima_venda:
            texto_recibo += (
                f"- {item['Produto']} | Qtd: {item['Quantidade']} | Preço Unit:"
                f" R$ {item['Preço Unit']:.2f} | Subtotal: R$"
                f" {item['Subtotal']:.2f}\n"
            )
          texto_recibo += (
              "========================================\nObrigado pela"
              " preferência!"
          )

          st.download_button(
              label="📄 Baixar Comprovativo",
              data=texto_recibo,
              file_name="comprovativo_venda.txt",
              mime="text/plain",
              use_container_width=True,
          )

        with col_pos2:
          df_ultima = pd.DataFrame(st.session_state.itens_ultima_venda)
          buffer_pos_excel = io.BytesIO()
          with pd.ExcelWriter(buffer_pos_excel, engine="openpyxl") as writer:
            df_ultima.to_excel(writer, index=False, sheet_name="Venda Fechada")
          buffer_pos_excel.seek(0)

          st.download_button(
              label="📥 Baixar Excel",
              data=buffer_pos_excel,
              file_name="venda_fechada.xlsx",
              mime=(
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              ),
              use_container_width=True,
          )

        with col_pos3:
          if whatsapp_cliente.strip():
            link_zap_pos = f"https://wa.me/{whatsapp_cliente}?text=Comprovativo%20da%20sua%20compra%20na%20farmacia:%20R${st.session_state.ultimo_total:.2f}"
          else:
            link_zap_pos = f"https://wa.me/?text=Comprovativo%20da%20compra:%20R${st.session_state.ultimo_total:.2f}"

          st.markdown(
              f"[💬 Enviar WhatsApp]({link_zap_pos})", unsafe_allow_html=True
          )

        if st.button("🔄 Nova Venda", use_container_width=True):
          st.session_state.venda_concluida = False
          st.rerun()
      else:
        st.info("O carrinho está vazio no momento.")

with aba_stock:
  st.subheader("📦 Gestão de Stock (Catálogo de 500+ Itens)")
  st.markdown(
      "Lista completa integrada de medicamentos disponíveis no balcão da"
      " farmácia:"
  )
  st.dataframe(
      st.session_state.stock, use_container_width=True, hide_index=True
  )

  # Botão para baixar todo o stock em Excel
  buffer_stock = io.BytesIO()
  with pd.ExcelWriter(buffer_stock, engine="openpyxl") as writer:
    st.session_state.stock.to_excel(writer, index=False, sheet_name="Stock")
  buffer_stock.seek(0)

  st.download_button(
      label="📥 Baixar Tabela de Stock Completa (.xlsx)",
      data=buffer_stock,
      file_name="stock_farmacia.xlsx",
      mime=(
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ),
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
        novo_item = pd.DataFrame({
            "Remédio": [novo_nome],
            "Categoria": [nova_cat],
            "Stock": [novo_qtd],
            "Preço (R$)": [novo_preco],
        })
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

  whatsapp_geral = st.text_input(
      "Número de WhatsApp para Envio de Fecho (Opcional - Ex: 5511999999999)",
      placeholder="5511999999999",
  )

  col_r1, col_r2, col_r3 = st.columns(3)
  with col_r1:
    # Relatório geral de stock em TXT/Relatório
    relatorio_txt = "=== RELATÓRIO GERAL DE STOCK - FARMÁCIA ===\n\n"
    relatorio_txt += st.session_state.stock.to_string(index=False)

    st.download_button(
        label="📄 Baixar Relatório Geral",
        data=relatorio_txt,
        file_name="relatorio_stock.txt",
        mime="text/plain",
        use_container_width=True,
    )

  with col_r2:
    buffer_rel_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_rel_excel, engine="openpyxl") as writer:
      st.session_state.stock.to_excel(
          writer, index=False, sheet_name="Relatorio Stock"
      )
    buffer_rel_excel.seek(0)

    st.download_button(
        label="📥 Descarregar Excel (.xlsx)",
        data=buffer_rel_excel,
        file_name="relatorio_stock.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        use_container_width=True,
    )

  with col_r3:
    if st.button("💬 Enviar Fecho via WhatsApp", use_container_width=True):
      if whatsapp_geral.strip():
        link_zap_geral = f"https://wa.me/{whatsapp_geral}?text=Relatorio%20de%20fecho%20de%20caixa%20da%20farmacia%20concluido%20com%20sucesso!"
      else:
        link_zap_geral = (
            "https://wa.me/?text=Relatorio%20de%20fecho%20de%20caixa%20da%20farmacia%20concluido%20com%20sucesso!"
        )

      st.markdown(
          f"[🔗 Clique aqui para abrir o WhatsApp]({link_zap_geral})",
          unsafe_allow_html=True,
      )
