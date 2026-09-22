import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

wb = openpyxl.Workbook()

# Aba 1: Painel de Controle (Dashboard)
ws_dash = wb.active
ws_dash.title = "Painel de Controle"
ws_dash.views.sheetView[0].showGridLines = True

# Aba 2: Estoque e Vendas
ws_inv = wb.create_sheet(title="Estoque e Vendas")
ws_inv.views.sheetView[0].showGridLines = True

# Aba 3: Fechamento de Caixa (PIX, Dinheiro, Cartão)
ws_caixa = wb.create_sheet(title="Fechamento de Caixa")
ws_caixa.views.sheetView[0].showGridLines = True

NAVY_HEADER = "0F172A"
LIGHT_BG = "F8FAFC"
WHITE = "FFFFFF"
GRAY_BORDER = "CBD5E1"
TEXT_DARK = "0F172A"

font_title = Font(name="Segoe UI", size=16, bold=True, color=TEXT_DARK)
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="64748B")
font_header = Font(name="Segoe UI", size=11, bold=True, color=WHITE)
font_bold = Font(name="Segoe UI", size=10, bold=True, color=TEXT_DARK)
font_normal = Font(name="Segoe UI", size=10, color=TEXT_DARK)

fill_header = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
fill_zebra = PatternFill(start_color=LIGHT_BG, end_color=LIGHT_BG, fill_type="solid")
fill_card = PatternFill(start_color="F0F9FF", end_color="F0F9FF", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color=GRAY_BORDER),
    right=Side(style='thin', color=GRAY_BORDER),
    top=Side(style='thin', color=GRAY_BORDER),
    bottom=Side(style='thin', color=GRAY_BORDER)
)

# --- MONTANDO O DASHBOARD ---
ws_dash['B2'] = "PAINEL DE CONTROLE - FARMÁCIA"
ws_dash['B2'].font = font_title
ws_dash['B3'] = "Sistema Completo para Gestão de Medicamentos, Estoque e Fluxo de Caixa"
ws_dash['B3'].font = font_subtitle

cards = [
    ("Total de Produtos", "=COUNTA('Estoque e Vendas'!B6:B100)", "B", "C"),
    ("Itens em Baixo Estoque", '=COUNTIF(\'Estoque e Vendas\'!H6:H100, "<= 10")', "E", "F"),
    ("Valor Total em Est.", "=SUM('Estoque e Vendas'!J6:J100)", "H", "I")
]

for title, formula, col1, col2 in cards:
    ws_dash.merge_cells(f"{col1}5:{col2}5")
    ws_dash.merge_cells(f"{col1}6:{col2}6")

    c_title = ws_dash[f"{col1}5"]
    c_title.value = title
    c_title.font = Font(name="Segoe UI", size=9, bold=True, color="0369A1")
    c_title.alignment = Alignment(horizontal="center", vertical="center")
    c_title.fill = fill_card

    c_val = ws_dash[f"{col1}6"]
    c_val.value = formula
    c_val.font = Font(name="Segoe UI", size=13, bold=True, color="0F172A")
    c_val.alignment = Alignment(horizontal="center", vertical="center")
    c_val.fill = fill_card

    for r in range(5, 7):
        for c in [ord(col1) - 64, ord(col2) - 64]:
            ws_dash.cell(row=r, column=c).border = thin_border

ws_dash['B9'] = "Orientações para o Operador / Balconista:"
ws_dash['B9'].font = font_bold
instructions = [
    "1. Digite novos produtos diretamente na aba 'Estoque e Vendas' (suporte a leitor de código de barras ou manual).",
    "2. Utilize a aba 'Fechamento de Caixa' para registrar as formas de pagamento (PIX, Dinheiro, Cartão).",
    "3. Sistema seguro, leve e preparado para operação profissional na farmácia."
]
for idx, text in enumerate(instructions, start=10):
    ws_dash[f"B{idx}"] = text
    ws_dash[f"B{idx}"].font = font_normal

# --- MONTANDO A ABA DE ESTOQUE E VENDAS ---
ws_inv['A2'] = "CONTROLE DE ESTOQUE E MEDICAMENTOS - FARMÁCIA"
ws_inv['A2'].font = font_title
ws_inv['A3'] = "Leitor de código de barras, cadastro manual e cálculo automático de estoque"
ws_inv['A3'].font = font_subtitle

headers_inv = [
    "ID", "Cód. Barras", "Nome do Medicamento / Produto", "Princípio Ativo / Apresentação",
    "Categoria", "Validade", "Preço de Venda (R$)", "Estoque Atual", "Custo Unitário (R$)", "Valor Total Estoque"
]

for col_idx, header in enumerate(headers_inv, start=1):
    cell = ws_inv.cell(row=5, column=col_idx)
    cell.value = header
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border
ws_inv.row_dimensions[5].height = 28

sample_data = [
    (1, "7891011121314", "Dipirona Sódica 500mg", "Dipirona Monoidratada - 30 Comprimidos", "Medicamento", "2028-12-15",
     12.50, 45, 4.00, "=G6*H6"),
    (2, "7891011121315", "Paracetamol 750mg", "Paracetamol - 20 Comprimidos", "Medicamento", "2027-10-10", 18.00, 8,
     6.50, "=G7*H7"),
    (3, "7891011121316", "Ibuprofeno 400mg", "Ibuprofeno - Cápsulas Gel", "Medicamento", "2027-06-20", 24.90, 30, 9.00,
     "=G8*H8"),
    (4, "7891011121317", "Amoxicilina 500mg", "Amoxicilina Tri-hidratada - 21 Cápsulas", "Antibiótico", "2026-11-05",
     42.00, 5, 18.00, "=G9*H9"),
    (5, "7891011121318", "Vitamina C 1g Efervescente", "Ácido Ascórbico - 10 Comprimidos", "Vitaminas", "2028-03-30",
     29.90, 15, 12.00, "=G10*H10"),
    (6, "7891011121319", "Omeprazol 20mg", "Omeprazol - 28 Cápulas", "Medicamento", "2027-08-12", 35.00, 12, 11.50,
     "=G11*H11"),
    (7, "7891011121320", "Soro Fisiológico 0,9% 500ml", "Cloreto de Sódio - Frasco", "Higiene / Soro", "2027-09-01",
     8.50, 50, 3.20, "=G12*H12")
]

for row_idx, row_data in enumerate(sample_data, start=6):
    for col_idx, val in enumerate(row_data, start=1):
        cell = ws_inv.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.font = font_normal
        cell.border = thin_border

        if col_idx in [1, 2, 6, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [7, 9, 10]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = 'R$ #,##0.00'
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

        if row_idx % 2 == 1:
            cell.fill = fill_zebra

for row_idx in range(13, 51):
    for col_idx in range(1, 11):
        cell = ws_inv.cell(row=row_idx, column=col_idx)
        cell.border = thin_border
        cell.font = font_normal
        if col_idx == 10:
            cell.value = f"=G{row_idx}*H{row_idx}"
            cell.number_format = 'R$ #,##0.00'
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif col_idx in [7, 9]:
            cell.number_format = 'R$ #,##0.00'
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif col_idx in [1, 2, 6, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

        if row_idx % 2 == 1:
            cell.fill = fill_zebra

dv_category = DataValidation(type="list", formula1='"Medicamento,Antibiótico,Vitaminas,Higiene / Soro,Cosméticos"',
                             allow_blank=True)
ws_inv.add_data_validation(dv_category)
dv_category.add("E6:E50")

red_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
red_font = Font(name="Segoe UI", size=10, bold=True, color="991B1B")
ws_inv.conditional_formatting.add("H6:H50",
                                  CellIsRule(operator="lessThanOrEqual", formula=["10"], stopIfTrue=True, fill=red_fill,
                                             font=red_font))

# --- MONTANDO A ABA DE FECHAMENTO DE CAIXA ---
ws_caixa['A2'] = "FECHAMENTO DE CAIXA - CONTROLE DE PAGAMENTOS"
ws_caixa['A2'].font = font_title
ws_caixa['A3'] = "Registro diário de entradas por PIX, Dinheiro e Cartões"
ws_caixa['A3'].font = font_subtitle

headers_caixa = ["Data", "Turno / Operador", "PIX (R$)", "Dinheiro (R$)", "Cartão Débito (R$)", "Cartão Crédito (R$)",
                 "Total Arrecadado"]

for col_idx, header in enumerate(headers_caixa, start=1):
    cell = ws_caixa.cell(row=5, column=col_idx)
    cell.value = header
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border
ws_caixa.row_dimensions[5].height = 28

sample_caixa = [
    ("2026-09-22", "Manhã - Balconista 1", 450.00, 230.00, 150.00, 320.00, "=SUM(C6:F6)"),
    ("2026-09-22", "Tarde - Balconista 2", 820.00, 410.00, 290.00, 580.00, "=SUM(C7:F7)"),
]

for row_idx, row_data in enumerate(sample_caixa, start=6):
    for col_idx, val in enumerate(row_data, start=1):
        cell = ws_caixa.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.font = font_normal
        cell.border = thin_border
        if col_idx in [3, 4, 5, 6, 7]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = 'R$ #,##0.00'
        else:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        if row_idx % 2 == 1:
            cell.fill = fill_zebra

for row_idx in range(8, 25):
    for col_idx in range(1, 8):
        cell = ws_caixa.cell(row=row_idx, column=col_idx)
        cell.border = thin_border
        cell.font = font_normal
        if col_idx in [3, 4, 5, 6]:
            cell.number_format = 'R$ #,##0.00'
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif col_idx == 7:
            cell.value = f"=SUM(C{row_idx}:F{row_idx})"
            cell.number_format = 'R$ #,##0.00'
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif col_idx == 1:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        if row_idx % 2 == 1:
            cell.fill = fill_zebra

# Linha de Totais do Caixa
total_row = 25
ws_caixa.cell(row=total_row, column=2, value="TOTAL GERAL").font = font_bold
ws_caixa.cell(row=total_row, column=2).alignment = Alignment(horizontal="right", vertical="center")
ws_caixa.cell(row=total_row, column=2).border = thin_border

for col_idx, col_letter in enumerate(["C", "D", "E", "F", "G"], start=3):
    cell = ws_caixa.cell(row=total_row, column=col_idx)
    cell.value = f"=SUM({col_letter}6:{col_letter}24)"
    cell.font = font_bold
    cell.number_format = 'R$ #,##0.00'
    cell.alignment = Alignment(horizontal="right", vertical="center")
    cell.border = thin_border

# Ajustes de largura
for ws in [ws_dash, ws_inv, ws_caixa]:
    for col in ws.columns:
        max_len = 0
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        for cell in col:
            if cell.value is not None:
                val_str = str(cell.value)
                if not val_str.startswith("=") and len(val_str) > max_len:
                    max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

ws_inv.column_dimensions['A'].width = 8
ws_inv.column_dimensions['B'].width = 18
ws_inv.column_dimensions['C'].width = 32
ws_inv.column_dimensions['D'].width = 36
ws_inv.column_dimensions['E'].width, ws_inv.column_dimensions['F'].width = 18, 14
ws_inv.column_dimensions['G'].width, ws_inv.column_dimensions['H'].width = 20, 16
ws_inv.column_dimensions['I'].width, ws_inv.column_dimensions['J'].width = 20, 22

ws_caixa.column_dimensions['A'].width = 15
ws_caixa.column_dimensions['B'].width = 25
ws_caixa.column_dimensions['C'].width, ws_caixa.column_dimensions['D'].width = 18, 18
ws_caixa.column_dimensions['E'].width, ws_caixa.column_dimensions['F'].width = 20, 20
ws_caixa.column_dimensions['G'].width = 22

file_name = "Sistema_Farmacia_Completo.xlsx"
wb.save(file_name)
print(f"File saved successfully as {file_name}")