mkdir docs

cat << 'EOF' > README.md
# Curvilinear Symbolic Calculator Tool

This repository implements a symbolic calculus engine and interactive web interface to perform asymptotic expansions for vector calculus operators in curvilinear coordinates. It is designed to automate the rigorous, multi-term mathematical expansions required for asymptotic analysis in phase-field modeling and related computational materials science fields.

### The Governing Mathematics

The tool calculates symbolic expansions for operators in a curvilinear coordinate system $(\rho, s)$. The spatial framework relies on a small parameter $\epsilon$ and curvature $K(s)$.

Where:
* $\rho$: The scaled normal coordinate, defined as $\rho = r/\epsilon$, where $r$ is the signed distance from the interface.
* $\epsilon$: The small parameter representing interface thickness.
* $K(s)$: The local interface curvature along the tangential coordinate $s$.
* $\mathbf{n}$ and $\mathbf{s}$: The normal and tangential basis vectors.

**Curvilinear Gradient:**
$$\nabla \phi = \mathbf{n} \left(\frac{1}{\epsilon}\frac{\partial \phi}{\partial \rho}\right) + \mathbf{s} \left(\frac{1}{1 + \epsilon \rho K}\frac{\partial \phi}{\partial s}\right)$$

![Curvilinear UI Screenshot](docs/ui_screenshot.png) 

### Project Architecture

* `core/symbolic_engine.py` : The backend SymPy engine containing the curvilinear vector calculus logic and expansion truncation rules.
* `app.py` : The Streamlit front-end architecture for the interactive web deployment.
* `requirements.txt` : Dependency definitions for Python environment reproduction.

### Installation

```bash
git clone [https://github.com/LingxiaS/Curvilinear-SymbolicCalc-tool.git](https://github.com/LingxiaS/Curvilinear-SymbolicCalc-tool.git)
cd Curvilinear-SymbolicCalc-tool
pip install -r requirements.txt
