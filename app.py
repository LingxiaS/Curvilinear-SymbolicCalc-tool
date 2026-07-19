import streamlit as st
import sympy as sp
from typing import List, Union, Tuple
from core.symbolic_engine import curvilinear_gradient, curvilinear_divergence, curvilinear_laplacian

st.set_page_config(page_title="Curvilinear Symbolic Expansion Tool", layout="wide")
st.title("Curvilinear Asymptotic Expansion Tool")
st.markdown("---")

st.header("Theory and Formula")
st.markdown("This tool performs asymptotic expansion for vector calculus operators in a curvilinear coordinate system $(\\rho, s)$, where $\\epsilon$ is the small parameter and $K(s)$ is the curvature.")
st.markdown(r"Here, $\rho = r/\epsilon$, where $r$ is the signed distance from the interface.")
st.markdown("The basis vectors are $\\mathbf{n}$ (normal) and $\\mathbf{s}$ (tangential).")

st.subheader("Curvilinear Gradient:")
st.latex(r'\nabla \phi = \mathbf{n} \left(\frac{1}{\epsilon}\frac{\partial \phi}{\partial \rho}\right) + \mathbf{s} \left(\frac{1}{1 + \epsilon \rho K}\frac{\partial \phi}{\partial s}\right)')

st.subheader("Curvilinear Divergence:")
st.latex(r'\nabla \cdot \mathbf{V} = \frac{1}{\epsilon} \frac{\partial V_n}{\partial \rho} + \frac{1}{1 + \epsilon \rho K} \left( \frac{\partial V_s}{\partial s} + K V_n \right)')
st.markdown("---")

st.sidebar.header("Calculation Parameters")
variable_name = st.sidebar.text_input("1. Variable Name (e.g., V, H):", value="H")
variable_type = st.sidebar.selectbox("2. Variable Type:", ("Scalar", "Vector"))

n_component_str, s_component_str = "0", "0"
op_choices = ["Gradient", "Laplacian"] if variable_type == "Scalar" else ["Divergence"]
operation_map = {"Gradient": "Gradient ($\nabla$)", "Laplacian": "Laplacian ($\nabla^2$)", "Divergence": "Divergence ($\nabla \cdot$)"}
operation_selection = st.sidebar.selectbox("3. Select Operator:", op_choices)
operation = operation_map[operation_selection] 

if variable_type == "Vector":
    st.sidebar.subheader("Vector Components")
    n_component_str = st.sidebar.text_input(f"Normal Component ($V_n$):", value="0")
    s_component_str = st.sidebar.text_input(f"Tangential Component ($V_s$):", value="0")

order = st.sidebar.number_input("4. Expansion Order (n, result up to $\\epsilon^n$):", min_value=0, value=1)
st.sidebar.markdown("---")
st.sidebar.subheader("Variable Expansion")
do_variable_expansion = st.sidebar.checkbox(f"5. Expand {variable_name} in $\\epsilon$", True)

expansion_terms: List[sp.Expr] = []
if do_variable_expansion:
    expansion_terms_area = st.sidebar.text_area("Expansion Terms (comma-separated, $V_0, V_1, ...$):", value="K(s), -rho * K(s)**2")
    try: expansion_terms = [sp.sympify(t.strip()) for t in expansion_terms_area.split(',')]
    except Exception: pass 

@st.cache_data
def execute_calculation(op_type, variable_name, v_type, n_comp_str, s_comp_str, _expansion_terms, order):
    rho, s, epsilon = sp.symbols('rho s epsilon')
    K, n_vec, s_vec = sp.Function('K')(s), sp.symbols(r'\mathbf{n} \mathbf{s}') 
    if v_type == "Scalar":
        phi = sp.sympify(0)
        if _expansion_terms:
            for i, term in enumerate(_expansion_terms): phi += term * (epsilon ** i)
        else: phi = sp.Function(variable_name)(rho, s)
        target_expr = phi
    else:
        target_expr = sp.sympify(n_comp_str) * n_vec + sp.sympify(s_comp_str) * s_vec

    if op_type == "Gradient ($\nabla$)": result_expr, op_symbol = curvilinear_gradient(target_expr, n_vec, s_vec, epsilon, rho, s, K, order), r"\nabla " + variable_name
    elif op_type == "Laplacian ($\nabla^2$)": result_expr, op_symbol = curvilinear_laplacian(target_expr, n_vec, s_vec, epsilon, rho, s, K, order), r"\nabla^2 " + variable_name
    else: result_expr, op_symbol = curvilinear_divergence(sp.sympify(n_comp_str), sp.sympify(s_comp_str), epsilon, rho, s, K, order), r"\nabla \cdot \mathbf{" + variable_name + "}"

    try:
        if n_vec in result_expr.free_symbols or s_vec in result_expr.free_symbols:
            expanded = result_expr.expand() 
            sorted_result = n_vec * sp.collect(expanded, n_vec).coeff(n_vec).series(epsilon, 0, order + 1).removeO() + s_vec * sp.collect(expanded, s_vec).coeff(s_vec).series(epsilon, 0, order + 1).removeO()
        else: sorted_result = result_expr.series(epsilon, 0, order + 1).removeO()
    except Exception: sorted_result = result_expr.subs(sp.Order(epsilon**(order + 1)), 0)
    return op_symbol, sp.latex(sorted_result), order

st.subheader("Result")
if st.sidebar.button("Execute Calculation"):
    if variable_name:
        with st.spinner(f"Calculating..."):
            op_symbol, latex_result, final_order = execute_calculation(operation, variable_name, variable_type, n_component_str, s_component_str, expansion_terms, order)
            st.success(f"Calculation Successful for ${op_symbol}$")
            st.latex(latex_result + r" + \mathcal{O}\left(\epsilon^{%s}\right)" % (final_order + 1))
