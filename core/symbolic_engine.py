import sympy as sp

def curvilinear_gradient(phi, n_vec, s_vec, epsilon, rho, s, K, order):
    series_order = order + 1 
    grad_rho = sp.expand(n_vec * (1/epsilon) * sp.diff(phi, rho))
    grad_s   = sp.expand(s_vec * (1/(1 + epsilon*rho*K)).series(epsilon, 0, series_order) * sp.diff(phi, s))
    return sp.expand(grad_rho + grad_s)

def curvilinear_divergence(n_component, s_component, epsilon, rho, s, K, order):
    series_order = order + 1
    n_dot_vec = n_component
    s_dot_vec = s_component
    term1 = sp.expand((1/epsilon) * sp.diff(n_dot_vec, rho))
    term2 = sp.expand((1/(1 + epsilon*rho*K)).series(epsilon, 0, series_order) * sp.diff(s_dot_vec, s))
    term3 = sp.expand((1/(1 + epsilon*rho*K)).series(epsilon, 0, series_order) * K * n_dot_vec)
    return sp.collect(term1 + term2 + term3, epsilon)

def curvilinear_laplacian(phi, n_vec, s_vec, epsilon, rho, s, K, order):
    grad_phi = curvilinear_gradient(phi, n_vec, s_vec, epsilon, rho, s, K, order)
    n_comp_grad = grad_phi.subs({s_vec: 0, n_vec: 1}) 
    s_comp_grad = grad_phi.subs({s_vec: 1, n_vec: 0})
    lap_phi = curvilinear_divergence(n_comp_grad, s_comp_grad, epsilon, rho, s, K, order)
    return sp.collect(lap_phi, epsilon)
