import streamlit as st

st.set_page_config(page_title="PAIF ContaLab", page_icon="📘", layout="wide")

# =========================
# CASOS
# =========================
CASES = {
    "HT1 - La Mascota Alegre": {
        "empresa": "La Mascota Alegre",
        "descripcion": """El día de hoy Usted decide iniciar la operación de un servicio de lavado de mascotas. 
Para ello, contacta a un amigo que le renta por un día un equipo especializado y además le entrega en consignación 
los materiales necesarios para realizar los lavados.

Ambos acuerdan que la renta del equipo se pagará al final del día por un monto de Q100. 
Asimismo, los materiales utilizados durante la jornada serán pagados hasta el día siguiente.

Se le solicita registrar las operaciones del día y elaborar los estados financieros correspondientes.""",
        "tx": [
            "1. Se inicia la operación con un aporte de capital de Q100.",
            "2. Durante el día se lavan 8 mascotas a razón de Q50 cada una, cobrando solamente un servicio de forma inmediata.",
            "3. Al finalizar la jornada, se paga la renta del equipo por Q100.",
            "4. Se registra el consumo de materiales utilizados, equivalente a Q80, los cuales serán pagados el día de mañana (cuenta por pagar)."
        ]
    },

    "HT2 - Second Chance": {
    "empresa": "Second Chance",
    "descripcion": """Se inicia la operación de una lavandería durante el día. 
Se realizan compras de materiales, contratación de servicios, gastos operativos 
y generación de ingresos tanto al contado como al crédito.

Al final del día, se debe determinar el resultado de la operación, la situación financiera 
y el flujo de efectivo de la empresa.""",
    "tx": [
        "1. Aporte inicial a la empresa por Q5,000, depositados en Banco de la Lavandería.",
        "2. Compra de materiales para lavado de ropa al contado, por Q1,000.",
        "3. Contratación de un local equipado para ser utilizado el día de hoy por Q200. La renta se pagará el día de mañana.",
        "4. Publicación de un pequeño volante anunciando la lavandería, pagado al contado por Q100.",
        "5. En el día se lavaron las siguientes prendas:",
        "   - 20 pantalones a Q15 c/u (contado)",
        "   - 25 camisas a Q10 c/u (contado)",
        "   - 10 blusas a Q12.50 c/u (crédito)",
        "6. Conteo de materiales sobrantes al final del día: Q700."
    ]
},

    "HT3 - Café Productivo": {
        "empresa": "Café Productivo",
        "descripcion": """Se inicia la operación de un servicio de asesoría técnica para productores de café. 
Durante el día se prestan servicios, se generan ingresos tanto cobrados como pendientes, 
y se incurre en distintos gastos necesarios para la operación.

Al cierre del día, existen obligaciones pendientes de pago que deben reconocerse como pasivos.

Se le solicita registrar las operaciones del día y elaborar los estados financieros correspondientes.""",
        "tx": [
            "1. Se realiza un aporte inicial de capital por Q3,000.",
            "2. Se generan ingresos por servicios prestados y cobrados en efectivo por Q2,500.",
            "3. Se registran ingresos adicionales por Q1,800 que aún no han sido cobrados (cuentas por cobrar).",
            "4. Se pagan gastos operativos por Q700.",
            "5. Se registran gastos por Q600 que serán pagados posteriormente (cuentas por pagar)."
        ]
    }
}

# =========================
# ESTADO
# =========================
def init():
    for k in [
        "t1","t2","t3","t4",
        "er_ingresos","er_materiales","er_alquiler",
        "evpn_aporte","evpn_utilidad",
        "bg_bancos","bg_cxc","bg_inv","bg_cxp",
        "bg_aporte","bg_utilidades",
        # RESULTADOS (IMPORTANTE)
        "chequera","utilidad","patrimonio",
        "activo","pasivo","patrimonio_bg","total_bg",
        "efe_flujo_neto"
    ]:
        if k not in st.session_state:
            st.session_state[k] = 0.0

init()

# =========================
# CÁLCULOS
# =========================
def calc():
    s = st.session_state

    # Chequera
    s.chequera = s.t1 + s.t2 + s.t3 + s.t4

    # ER
    s.utilidad = s.er_ingresos + s.er_materiales + s.er_alquiler

    # EVPN
    s.patrimonio = s.evpn_aporte + s.evpn_utilidad

    # BG
    s.activo = s.bg_bancos + s.bg_cxc + s.bg_inv
    s.pasivo = s.bg_cxp
    s.patrimonio_bg = s.bg_aporte + s.bg_utilidades
    s.total_bg = s.pasivo + s.patrimonio_bg

    # =========================
    # EFE CORRECTO
    # =========================
    s.efe_flujo_neto = (
        s.utilidad
        - abs(s.bg_cxc)     # 👈 RESTA
        - abs(s.bg_inv)     # 👈 RESTA
        + abs(s.bg_cxp)     # 👈 SUMA
        + abs(s.bg_aporte)  # 👈 SUMA
    )

calc()

# =========================
# UI
# =========================
st.title("PAIF ContaLab")

case = st.selectbox("Ejercicio", list(CASES.keys()))
c = CASES[case]

st.subheader(c["empresa"])
st.write(c["descripcion"])

st.markdown("### Transacciones")
for t in c["tx"]:
    st.write("-", t)

# =========================
# GRID
# =========================
col1, col2, col3, col4 = st.columns(4)

# CHEQUERA
with col1:
    st.markdown("### Chequera")
    st.number_input("Aporte", key="t1")
    st.number_input("Ingresos", key="t2")
    st.number_input("Gastos 1", key="t3")
    st.number_input("Gastos 2", key="t4")
    st.success(f"{st.session_state.chequera:.2f}")

# ER
with col2:
    st.markdown("### ER")
    st.number_input("Ingresos", key="er_ingresos")
    st.number_input("Gastos 1", key="er_materiales")
    st.number_input("Gastos 2", key="er_alquiler")
    st.success(f"{st.session_state.utilidad:.2f}")

# EVPN
with col3:
    st.markdown("### EVPN")
    st.number_input("Aporte", key="evpn_aporte")
    st.number_input("Utilidad", key="evpn_utilidad")
    st.success(f"{st.session_state.patrimonio:.2f}")

# BG
with col4:
    st.markdown("### BG")

    st.markdown("**Activo**")
    st.number_input("Bancos", key="bg_bancos")
    st.number_input("Cuentas por cobrar", key="bg_cxc")
    st.number_input("Inventarios", key="bg_inv")
    st.write("Total Activo:", st.session_state.activo)

    st.markdown("**Pasivo**")
    st.number_input("Cuentas por pagar", key="bg_cxp")
    st.write("Total Pasivo:", st.session_state.pasivo)

    st.markdown("**Patrimonio**")
    st.number_input("Aporte", key="bg_aporte")
    st.number_input("Utilidades", key="bg_utilidades")
    st.write("Total Patrimonio:", st.session_state.patrimonio_bg)

    st.success(f"Pasivo + Patrimonio = {st.session_state.total_bg:.2f}")

# =========================
# CONTROL CONTABLE
# =========================
st.markdown("### Control contable")

dif = st.session_state.activo - st.session_state.total_bg

if abs(dif) < 0.01:
    st.success("✔ Balance correcto: Activo = Pasivo + Patrimonio")
else:
    st.error(f"✖ Descuadre: diferencia de {dif:.2f}")

# =========================
# EFE CON SIGNOS
# =========================
st.markdown("### Estado de Flujo de Efectivo")

s = st.session_state

st.write(f"Utilidad: {s.utilidad:.2f}")
st.write(f"(-) Cuentas por cobrar: {-abs(s.bg_cxc):.2f}")
st.write(f"(-) Inventarios: {-abs(s.bg_inv):.2f}")
st.write(f"(+) Cuentas por pagar: {abs(s.bg_cxp):.2f}")
st.write(f"(+) Aporte: {abs(s.bg_aporte):.2f}")

# =========================
# EXPORTAR A EXCEL
# =========================
from io import BytesIO
import pandas as pd

st.markdown("### Descargar hoja")

if st.button("Descargar Excel"):

    s = st.session_state

    data = [
        ["--- CHEQUERA ---", ""],
        ["Aporte", s.t1],
        ["Ingresos", s.t2],
        ["Renta", s.t3],
        ["Materiales", s.t4],
        ["Total Chequera", s.chequera],

        ["", ""],
        ["--- ER ---", ""],
        ["Ingresos", s.er_ingresos],
        ["Materiales", s.er_materiales],
        ["Alquiler", s.er_alquiler],
        ["Utilidad", s.utilidad],

        ["", ""],
        ["--- EVPN ---", ""],
        ["Aporte", s.evpn_aporte],
        ["Utilidad", s.evpn_utilidad],
        ["Patrimonio", s.patrimonio],

        ["", ""],
        ["--- BG ---", ""],
        ["Activo", s.activo],
        ["Pasivo", s.pasivo],
        ["Patrimonio", s.patrimonio_bg],
        ["Total BG", s.total_bg],

        ["", ""],
        ["--- EFE ---", ""],
        ["Utilidad", s.utilidad],
        ["(-) CxC", -abs(s.bg_cxc)],
        ["(-) Inventarios", -abs(s.bg_inv)],
        ["(+) CxP", abs(s.bg_cxp)],
        ["(+) Aporte", abs(s.bg_aporte)],
        ["Flujo de efectivo", s.efe_flujo_neto],
    ]

    df = pd.DataFrame(data, columns=["Concepto", "Valor"])

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="PAIF")

    st.download_button(
        label="Descargar archivo Excel",
        data=buffer.getvalue(),
        file_name="PAIF_ContaLab.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.success(f"Flujo de efectivo: {s.efe_flujo_neto:.2f}")

# =========================
# LIMPIAR HOJA
# =========================
st.markdown("### Reiniciar hoja")

if st.button("Limpiar todos los datos"):

    for k in list(st.session_state.keys()):
        del st.session_state[k]

    st.rerun()
