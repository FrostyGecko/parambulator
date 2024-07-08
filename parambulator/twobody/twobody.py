import numpy as np
import pandas as pd
import parambulator.data.planet_data as planet_data

deg2rad = np.pi/180  # [rad/deg]
rad2deg = 180/np.pi  # [deg/rad]

def Orbit_Normal_Vector(RAAN,inc):
    
    RAAN    = np.deg2rad(RAAN)
    inc     = np.deg2rad(inc)
    
    A = np.matrix([[np.cos(RAAN), -np.sin(RAAN),  0],
                   [np.sin(RAAN), np.cos(RAAN),   0],
                   [0,           0,               1]])
   
    B = np.matrix([[1, 0, 0],
                   [0, np.cos(inc), -np.sin(inc)],
                   [0, np.sin(inc), np.cos(inc)]])
   
    n = np.matrix([[0],
                   [0],
                   [1]])
                   
    O_hat = A @ B @ n
    
    return O_hat
    

def InverseSquare(I0,R0,R1):
    return I0*((R0**2)/(R1**2))
    
def GravAcc(G,r,m1,m2):
    return G*(m1*m2)/(r**2)

def LagrangeFG(R0,V0,delta_nu,mu):
    
    delta_nu = delta_nu*(3.1415926/180)
    
    #### Calculate F&G parameters
    r0      = np.linalg.norm(R0)
    h       = np.linalg.norm(np.cross(R0, V0))
    v0r     = (np.dot(R0,V0))/np.linalg.norm(R0)
    r       = (h**2/mu)/(1 + (h**2/(mu*r0) - 1)*np.cos(delta_nu) - (h*v0r*np.sin(delta_nu))/mu)
    
    #### Calculate f,g,fdot,gdot
    f       = 1 - (mu*r*(1 - np.cos(delta_nu)))/(h**2)
    g       = r*r0*np.sin(delta_nu)/h
    f_dot_1 = (mu/h)*((1-np.cos(delta_nu))/np.sin(delta_nu))
    f_dot_2 = (mu/h**2)*(1 - np.cos(delta_nu)) - 1/r0 - 1/r
    f_dot   = f_dot_1*f_dot_2
    g_dot   = 1 - ((mu*r0)/h**2)*(1 - np.cos(delta_nu))
    
    FG      = pd.Series([f,g,f_dot,g_dot])
    index   = ['f','g','f_dot','g_dot']
    FG.index = index
    
    return FG

def LagrangeFG_NextState(R0,V0,FG):
    R1  = FG['f']*R0 + FG['g']*V0
    V1  = FG['f_dot']*R0 + FG['g_dot']*V0
    
    return R1, V1

def Vescape(r_mag,mu):
    return np.sqrt((2*mu)/r_mag)

def tbp0000_EccVec_1(R,V,mu=planet_data.earth['mu']):
    
    h_vec   = np.cross(R, V)
    e_vec   = np.cross(V,h_vec)/mu - R/np.linalg.norm(R)
    
    return e_vec

def tbp0000_Ecc(R,V,mu=planet_data.earth['mu']):
    
    h_vec   = np.cross(R, V)
    e_vec   = np.cross(V,h_vec)/mu - R/np.linalg.norm(R)
    e       = np.linalg.norm(e_vec)
    return e

def tbp0000_SemiLatusRectum(R,V,mu=planet_data.earth['mu']):
    r_mag   = np.linalg.norm(R)
    v_mag   = np.linalg.norm(V)
    h_vec   = np.cross(R, V)
    h_mag   = np.linalg.norm(h_vec)
    p       = (h_mag**2)/mu
    return p
    
    
def tbp0000_semi_major_axis_1(specific_energy,mu=planet_data.earth['mu']):
    return -mu/(2*specific_energy)
    
def tbp0000_semi_major_axis_1():
    pass

def tbp0000_ecc_1():
    pass

def tbp0000_orbit_shape(R,V,mu=planet_data.earth['mu']):
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    h_vec           = np.cross(R, V)
    h               = np.linalg.norm(h_vec)
    specific_energy = (v**2/2) - mu/r
    a               = -mu/(2*specific_energy)
    e               = ((h**2)/(mu*r) - 1) 
    i               = np.acos(h_vec[2]/h)
    
    return [a,e,i]


def tbp0000_node_vector_1(R,V):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.

    Returns
    -------
    N : TYPE
        DESCRIPTION.

    '''
    h_vec   = np.cross(R, V)
    K       = np.array([0,0,1])
    N       = np.cross(K,h_vec)
    
    return N
            


def tbp0000_Cart_to_Kepler(R,V,mu=planet_data.earth['mu']):
    
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    H               = np.cross(R, V)
    h               = np.linalg.norm(H)
    e_vec           = tbp0000_EccVec_1(R,V,mu)
    specific_energy = (v**2)/2 - mu/r
    a               = -mu/(2*specific_energy)
    i               = np.arccos(H[2]/h)
    e               = ((h**2)/(mu*r) - 1)    
    p               = h**2/mu
    P               = (2*np.pi*(a**(3/2)))/np.sqrt(mu)
    r_p             = a*(1-e)
    r_a             = a*(1+e)
    K               = np.array([0,0,1])
    N               = np.cross(K,H)
    n               = np.linalg.norm(N)
    
    #### Right Ascension of the Ascending Node
    RAAN            = np.arccos(N[0]/n)
    
    if N[1] > 0:
        RAAN = np.pi - RAAN
        
    #### Argument of Periapsis
    omega           = np.arccos(np.dot(N,e_vec)/(n*e))
    
    #### True Anomaly
    if e_vec[2] > 0:
        omega = np.pi - omega
    
    e_vec_dot_R = np.dot(e_vec,R)
    nu          = np.arccos(e_vec_dot_R/(e*r))
    
    #### Argument of Latitude at Epoch
    if e_vec_dot_R > 0:
        nu = np.pi - nu
    
    arg_lat_epoch = np.arccos(np.dot(N,R)/(n*r))
    
    #### True Longitude at Epoch
    if R[2] > 0:
        arg_lat_epoch = np.pi - arg_lat_epoch
        
    true_long_epoch     = RAAN+omega+nu
    
    #### Compile Keplerian Elements
    kep_elements  = {
                'a':        a,
                'e':        e,
                'i':        i*rad2deg,
                'RAAN':     RAAN*rad2deg,
                'omega':    omega*rad2deg,
                'nu':       nu*rad2deg,
                'P':        P,
                'e_vec':    e_vec,
                'specific_energy': specific_energy,
                'p':        p,
                'h':        h,
                'r_p':      r_p,
                'r_a':      r_a,
                'arg_lat_epoch':arg_lat_epoch*rad2deg,
                'true_long_epoch':true_long_epoch*rad2deg,
                
        }

    return kep_elements

    
def PeriapsisVec(R,V,mu):
    
    e_vec           = tbp0000_EccVec_1(R,V,mu)
    e               = np.linalg.norm(e_vec)
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    specific_energy = (v**2/2) - mu/r
    a               = -mu/(2*specific_energy)
    p_hat           = e_vec/np.linalg.norm(e_vec)
    r_p_vec         = a*(1-e)*p_hat
    
    return r_p_vec

def ApoapsisVec(R,V,mu):
    
    e_vec           = tbp0000_EccVec_1(R,V,mu)
    e               = np.linalg.norm(e_vec)
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    specific_energy = (v**2/2) - mu/r
    a               = -mu/(2*specific_energy)
    p_hat           = e_vec/np.linalg.norm(e_vec)
    r_a_vec         = -a*(1+e)*p_hat
    
    return r_a_vec