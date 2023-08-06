import numpy as np

def k2j(k, E, nu, plane_stress=False):
    """
    Convert fracture 
    
    Parameters
    ----------
    k: float
    E: float
        Young's modulus in GPa.
    nu: float
        Poisson's ratio
    plane_stress: bool
        True for plane stress (default) or False for plane strain condition.
    
    Returns
    -------
    float
    
    """
    
    if plane_stress:
        E = E / (1 - nu ** 2)
        
    return k ** 2 / E


def j2k(j, E, nu, plane_stress=True):
    """
    Convert fracture 
    
    Parameters
    ----------
    j: float (in N/mm)
    E: float
        Young's modulus in GPa.
    nu: float
        Poisson's ratio
    plane_stress: bool
        True for plane stress (default) or False for plane strain condition.
    
    Returns
    -------
    K : float
        Units are MPa m^0.5.
    """
    
    if plane_stress:
        E = E / (1 - nu ** 2)
        
    return (j * E) ** 0.5

def calc_cpf(data):
    data_ordered = np.sort(data)
    u =  (np.arange(len(data)) + 1 - 0.3) / (len(data) + 0.4)
    
    return data_ordered, u

def find_closest(a, b, x, tol=0.01):
    """
    For two arrays `a` and `b`, find the elements in `b` closest to the `x` element in `a`.
    
    Parameters
    ----------
    a: narray of shape (N,)
    b: narray of shape (N,)
    x: float
    tol: float
        Tolerance value. 
    Returns
    -------
    """
    a_idx = np.isclose(a, x, atol=tol)
    a_i = a[a_idx]
    b_i = b[a_idx]

    return a_i, b_i
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def thinf(Ltild, tau, T):
    kb =  1.3806498e-23 # J/K
    b=0.248e-9
    Uk=0.33 * 1.60217657e-19
    rho = 1e14
#      lstar(tau* 1e6, temps[i] + 273)* 1e6
    
    epsdot = np.zeros(len(tau))
    idx_more = lstar(tau*1e6, T) > np.ones(len(lstar(tau*1e6, T))) * Ltild
    idx_less = ~idx_more
#     print(T[idx_more].shape)
#     print(Fk(tau, T)[idx_more].shape)
#     print('Lastar: ', lstar(tau*1e6, T)* 1e6)
#     print('idx_more: ', idx_more)

#     norm_factor =  np.exp(-Uk / (kb * T))
    norm_factor =  1 / (2 * Fk(np.array([0]), -200+273.15) / (kb * (-200+273.15)))[0]

#     epsdot[idx_more] = norm_factor * np.exp(Fk(tau, T)[idx_more] / (kb * T))
#     epsdot[idx_less] = norm_factor * np.exp(Fk(tau, T)[idx_less] / (kb * T)) 
    
#     norm_factor = 1/8.716293226522263e-20
    epsdot[idx_more] = norm_factor * 2 * Fk(tau, T)[idx_more] / (kb * T) 
    epsdot[idx_less] = norm_factor * Fk(tau, T)[idx_less] / (kb * T)

#     epsdot[idx_more] = 1 / (rho * b * Ltild * np.exp(- 2 * Fk(tau, T)[idx_more] / (kb * T)))
#     epsdot[idx_less] = 1 / (rho * b * b * np.exp(- Fk(tau, T)[idx_less] / (kb * T)))
    
#     epsdot[idx_more] = 1e-16 / (rho * b * b * np.exp(- Fk(tau, T)[idx_more] / (kb * T)))
#     epsdot[idx_less] = 1e-16 / (rho * b * b * np.exp(- Fk(tau, T)[idx_less] / (kb * T)))
    
#     epsdot[idx_more] = np.exp(Fk(tau, T)[idx_more] / (kb * T))
#     epsdot[idx_less] = np.exp(Fk(tau, T)[idx_less] / (kb * T)) 

        
    return epsdot