import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

import functions as func

try:
    import os
    os.system('clear')
    plt.close("all")
except:  
    pass
    
#%% Initialize
class Thermal():
    def __init__(self):
        self.solar_flux_hot     = 1414
        self.solar_flux_nom     = 1367
        self.solar_flux_cold    = 1314
        
        self.earthIR_flux_hot   = 260
        self.earthIR_flux_nom   = 240
        self.earthIR_flux_cold  = 220
        
        self.albedo_hot         = 0.4
        self.albedo_nom         = 0.3
        self.albedo_cold        = 0.2
        
        #### Run Self Functions
        self.SELF_initialize()
        
    def SELF_initialize(self):
        self.Calc_Albedo_Flux()
        
        
    def Calc_Albedo_Flux(self):
        self.albedo_flux_hot    = self.solar_flux_hot*self.albedo_hot
        self.albedo_flux_nom    = self.solar_flux_nom*self.albedo_nom
        self.albedo_flux_cold   = self.solar_flux_cold*self.albedo_cold
        
class CR2BP():
    def __init__(self,
                 a = 10000,
                 e = 0.0001,
                 inc=51.6,
                 alt=400,
                 RAAN=0
                 ):
        
        
        self.altitude           = alt
        self.eccentricity       = e
        self.semi_major_axis    = a
        self.inc                = inc
        self.RAAN               = RAAN
        self.Earth_radius       = 6378.137
        self.Earth_radius_polar = 6356751.9
        self.Earth_radius_eq    = 6378136.6
        self.obl_ecl            = 23.45
        self.Earth_omega        = 7.292115*(10**(-5))     # rad/s
        self.oblateness         = (self.Earth_radius_eq - self.Earth_radius_polar)/self.Earth_radius_eq
        self.Earth_mass         = 5.972*(10**24)
        self.G                  = 6.67430*(10**(-11))
    
        
    def Solar_Vector(self,Gamma):
        
        obl_ecl = np.deg2rad(self.obl_ecl)
        Gamma   = np.deg2rad(Gamma)
        
        A = np.matrix([[1, 0, 0],
                       [0, np.cos(obl_ecl), -np.sin(obl_ecl)],
                       [0, np.sin(obl_ecl), np.cos(obl_ecl)]])
       
        B = np.matrix([[np.cos(Gamma), -np.sin(Gamma),  0],
                       [np.sin(Gamma),  np.cos(Gamma),  0],
                       [0,           0,                 1]])
       
        n = np.matrix([[1],
                       [0],
                       [0]])
                       
        S_hat = A @ B @ n
        
        return S_hat
        
    def Orbit_Normal_Vector(self,RAAN,inc):
        
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
        
    def Beta_Angle(self,RAAN,inc,Gamma):
        S_hat       = self.Solar_Vector(Gamma)
        O_hat       = self.Orbit_Normal_Vector(RAAN,inc)
        psi         = np.transpose(O_hat) @ S_hat
        beta_angle  = np.rad2deg(np.arcsin(psi))[0,0]
        
        return beta_angle
    

    def EclipseTimes(self,beta,alt):
        beta    = np.deg2rad(beta)
        alt     = alt
        r_e     = self.body_radius
        theta   = np.sqrt( (1/(np.cos(beta)**2)) * ( (r_e/(r_e + alt))**2 - np.sin(beta)**2))
        
        return np.rad2deg(theta)
    
    def RAAN_procession(self,omega):
        inc     = np.deg2rad(self.inc)
        a       = self.semi_major_axis
        e       = self.eccentricity
        R_e     = self.Earth_radius
        J2      = self.J2()
        omega_p = - (3 * R_e**2 * J2 * omega * np.cos(inc))/(2 * (a*(1-e**2))**2)
        
        return np.rad2deg(omega_p)
    
    def J2(self):
        oblateness  = self.oblateness
        Earth_omega = self.Earth_omega
        R_e         = self.Earth_radius_eq
        M_e         = self.Earth_mass
        G           = self.G
        
        return (2*oblateness)/3 - ((R_e)**3 * Earth_omega**2)/(3*G*M_e)

    def InverseSquare(self,I0,R0,R1):
        return I0*((R0**2)/(R1**2))
    
        
    def GravAcc(self,r,m1,m2):
        G = self.G
        return G*(m1*m2)/(r**2)
    
    def VecDiff(self,vec_i,vec_j):
        return vec_j - vec_i
    
    def VecMul1D(self,vec1,vec2):
        return np.transpose(vec1) @ vec2
    
    def LagrangeFG(self,R0,V0,delta_nu,mu):
        
        delta_nu = delta_nu*(3.1415926/180)
        
        #### Calculate F&G parameters
        r0      = np.linalg.norm(R0)
        h       = np.linalg.norm(np.cross(R0, V0))
        v0r     = (np.dot(R0,V0))/np.linalg.norm(R0)
        r       = (h**2/mu)/(1 + (h**2/(mu*r0) - 1)*np.cos(delta_nu) - (h*v0r*np.sin(delta_nu))/mu)
        e       = ((h**2)/(mu*r) - 1)
        
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
    
    def LagrangeFG_NextState(self,R0,V0,FG):
        R1  = FG['f']*R0 + FG['g']*V0
        V1  = FG['f_dot']*R0 + FG['g_dot']*V0
        
        return R1, V1
    
    def Vescape(self,r_mag,mu):
        return np.sqrt((2*mu)/r_mag)
    
    def Cart_to_Kepler(self,R,V):
        r               = np.linalg.norm(R)
        v               = np.linalg.norm(V)
        h_vec           = np.cross(R, V)
        h               = np.linalg.norm(h_vec)
        specific_energy = (v**2/2) - mu/r
        a               = -mu/(2*specific_energy)
        i               = np.acos(h_vec[2])/h
        
        
        r_p             = a*(1-e)
        r_a             = a*(1+e)
        
        p       = h**2/mu
        
        return True
    
    def EccentricityVector(self,R,V,mu):
        h_vec   = np.cross(R, V)
        e_vec   = np.cross(V,h_vec)/mu - R/np.linalg.norm(R)
        
        return e_vec
    
    def CircularVelocity(self,radius,mu):
        return np.sqrt(mu/radius)
        
    def PeriapsisVector(self,R,V,mu):
        
        e_vec           = self.EccentricityVector(R,V,mu)
        e               = np.linalg.norm(e_vec)
        r               = np.linalg.norm(R)
        v               = np.linalg.norm(V)
        specific_energy = (v**2/2) - mu/r
        a               = -mu/(2*specific_energy)
        p_hat           = e_vec/np.linalg.norm(e_vec)
        r_p_vec         = a*(1-e)*p_hat
        
        return r_p_vec
    
    def ApoapsisVector(self,R,V,mu):
        
        e_vec           = self.EccentricityVector(R,V,mu)
        e               = np.linalg.norm(e_vec)
        r               = np.linalg.norm(R)
        v               = np.linalg.norm(V)
        specific_energy = (v**2/2) - mu/r
        a               = -mu/(2*specific_energy)
        p_hat           = e_vec/np.linalg.norm(e_vec)
        r_a_vec         = -a*(1+e)*p_hat
        
        return r_a_vec
        
orbit   = CR2BP()

RAAN    = 0
inc     = 51.6
Gamma   = 0
BA      = orbit.Beta_Angle(RAAN, inc, Gamma)


R0  = np.array([6378.1366+600, 0, 0])
V0  = np.array([0, 7.557935209925521, 1.5])
mu  = 398600

r_p_vec     = orbit.PeriapsisVector(R0,V0,mu)
r_a_vec     = orbit.ApoapsisVector(R0,V0,mu)

delta_nu_vec = np.linspace(1,361,361)

Rvec = np.zeros([len(delta_nu_vec),3])
Vvec = np.zeros([len(delta_nu_vec),3])

for i,delta_nu in enumerate(delta_nu_vec):
    FG = orbit.LagrangeFG(R0,V0,delta_nu,mu)
    Rvec[i], Vvec[i] = orbit.LagrangeFG_NextState(R0,V0,FG)

    
orbit_radius_vec    = np.linalg.norm(Rvec,axis=1)
altitude_vec        = orbit_radius_vec - 6378.1366

#### Initialize Figure
fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),constrained_layout=1)

#### Plot Primary
theta, phi = np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 40)
THETA, PHI = np.meshgrid(theta, phi)
R_eq    = 6378.1366
R_polar = 6356.7519
X       = R_eq * np.sin(PHI) * np.cos(THETA)
Y       = R_eq * np.sin(PHI) * np.sin(THETA)
Z       = R_polar * np.cos(PHI)
ax.plot_surface(X, Y, Z,cmap=plt.get_cmap('jet'),zorder=1)

#### Plot Periapsis
x, y, z = [0, r_p_vec[0]], [0, r_p_vec[1]], [0, r_p_vec[2]]
ax.scatter(x, y, z, c='red', s=1)
ax.plot(x, y, z, color='black')

#### Plot Apoapsis
x, y, z = [0, r_a_vec[0]], [0, r_a_vec[1]], [0, r_a_vec[2]]
ax.scatter(x, y, z, c='red', s=1)
ax.plot(x, y, z, color='black')

#### Plot Orbit
ax.plot3D(Rvec[:,0],Rvec[:,1],Rvec[:,2],zorder=2)

#### Plot Solar Vector
S = np.array([[0, 10000], [0, 10000], [0, 0]])
ax.scatter(S[0], S[1], S[2], c='red', s=1)
ax.plot(S[0], S[1], S[2], color='red',zorder=1)


#### Plot Position

eclipse = np.zeros(len(Rvec))
for i in range(0,len(Rvec)):
    Q       = np.array([Rvec[i,0],Rvec[i,1],Rvec[i,2]])
    R       = Q+S[:,1]
    R_vec   = np.array([[Q[0] + 0, Q[0]+10000], 
                        [Q[1] + 0, Q[1]+10000], 
                        [Q[2] + 0, Q[2]+0]])
    P       = np.array([0,0,0])
    t       = np.dot((R-Q),(Q-P))/np.dot((R-Q),(R-Q))
    G       = Q-t*(R-Q)
    
    D       = S[:,1] - Q
    F       = G - Q
    H       = np.divide(F,D)

    if np.linalg.norm(G) < 6378.1366:
        eclipse[i] = 1
    else:
        eclipse[i] = 0
    

#### Options
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=20)
ax.set_title('3D Orbit')
ax.set_aspect("equal")
ax.grid()
plt.show()



I0      = 250
R0      = 6878

I1_vec  = orbit.InverseSquare(I0,R0,orbit_radius_vec)
    
fig = plt.figure()
plt.plot(I1_vec)
plt.ylim([0,300])
plt.grid()



