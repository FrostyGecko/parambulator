#%% Initialize
import numpy as np
import matplotlib.pyplot as plt 
import os
import seaborn as sb

#### Set Printing
np.set_printoptions(suppress=True, precision=6)

#### Import Orbit Dependancies
from jplephem.spk import SPK
import juliandate as jd
import astropy as ap
from astropy.time import Time

#### System Clear
try:
    os.system('clear')
    plt.close("all")
except:  
    pass

#%% Get SPK File Location
spk_filepath = 'data/spk_files/de440_mars.bsp'
spk_filepath = 'data/spk_files/de421.bsp'

#https://github.com/AndrewAnnex/SpiceyPy
#https://github.com/skyfielders/python-skyfield/
#https://space.stackexchange.com/questions/51068/is-it-posible-to-convert-jpl-horizons-vectors-to-ecef/51077?noredirect=1

t = Time('2000-01-1 12:00:00', scale='utc')

print(t.tdb.value)
print(jd.to_gregorian(t.jd))


#%% Get Ephemeris using jplephem
# https://pypi.org/project/jplephem/

def load_kernel(spk_filepath):
    return SPK.open(spk_filepath)

kernel = load_kernel(spk_filepath)
print('-----kernel options-----')
print(kernel)

#### Get coordinates of Mars(4) with respet to SS barycenter(0)at midnight on  2015 February 8 TDB (barycentric Dynamical Time) which is Julian date 2457061.
print('-----Mars wrt SS barycenter-----')
position = kernel[0,4].compute(2457061.5)
print('Position (km):')
print(position)




def get_sun_position_ICRF(kernel,julian_date):
    Sun_position        = kernel[0,10].compute(julian_date)
    return Sun_position

def get_mercury_position_ICRF(kernel,julian_date):
    Mercury_position    = kernel[0,1].compute(julian_date)
    return Mercury_position

def get_venus_position_ICRF(kernel,julian_date):
    Venus_position      = kernel[0,2].compute(julian_date)
    return Venus_position

def get_earth_position_ICRF(kernel,julian_date):
    Earth_position      = kernel[0,3].compute(julian_date)
    Earth_position      -= kernel[3,399].compute(julian_date)
    return Earth_position

def get_earth_barycenter_position_ICRF(kernel,julian_date):
    Earth_barycenter      = kernel[0,3].compute(julian_date)
    return Earth_barycenter
    
def get_mars_position_ICRF(kernel,julian_date):
    Mars_position       = kernel[0,4].compute(julian_date)
    return Mars_position

def get_jupiter_position_ICRF(kernel,julian_date):
    Jupiter_position    = kernel[0,5].compute(julian_date)
    return Jupiter_position

def get_saturn_position_ICRF(kernel,julian_date):
    Saturn_position     = kernel[0,6].compute(julian_date)
    return Saturn_position

def get_uranus_position_ICRF(kernel,julian_date):
    Uranus_position     = kernel[0,7].compute(julian_date)
    return Uranus_position

def get_neptune_position_ICRF(kernel,julian_date):
    Neptune_position    = kernel[0,8].compute(julian_date)
    return Neptune_position

def get_pluto_position_ICRF(kernel,julian_date):
    Pluto_position      = kernel[0,9].compute(julian_date)
    return Pluto_position


#### Get Velocity
def get_sun_velocity_ICRF(kernel,julian_date):
    Sun_position        = kernel[0,10].compute_and_differentiate(julian_date)
    return Sun_position

def get_mercury_velocity_ICRF(kernel,julian_date):
    Mercury_position    = kernel[0,1].compute_and_differentiate(julian_date)
    return Mercury_position

def get_venus_velocity_ICRF(kernel,julian_date):
    Venus_position      = kernel[0,2].compute_and_differentiate(julian_date)
    return Venus_position

def get_earth_velocity_ICRF(kernel,julian_date):
    Earth_position      = kernel[0,3].compute_and_differentiate(julian_date)
    Earth_position      -= kernel[3,399].compute_and_differentiate(julian_date)
    return Earth_position

def get_earth_barycenter_velocity_ICRF(kernel,julian_date):
    Earth_barycenter      = kernel[0,3].compute_and_differentiate(julian_date)
    return Earth_barycenter
    
def get_mars_velocity_ICRF(kernel,julian_date):
    Mars_position       = kernel[0,4].compute_and_differentiate(julian_date)
    return Mars_position

def get_jupiter_velocity_ICRF(kernel,julian_date):
    Jupiter_position    = kernel[0,5].compute_and_differentiate(julian_date)
    return Jupiter_position

def get_saturn_velocity_ICRF(kernel,julian_date):
    Saturn_position     = kernel[0,6].compute_and_differentiate(julian_date)
    return Saturn_position

def get_uranus_velocity_ICRF(kernel,julian_date):
    Uranus_position     = kernel[0,7].compute_and_differentiate(julian_date)
    return Uranus_position

def get_neptune_velocity_ICRF(kernel,julian_date):
    Neptune_position    = kernel[0,8].compute_and_differentiate(julian_date)
    return Neptune_position

def get_pluto_velocity_ICRF(kernel,julian_date):
    Pluto_position      = kernel[0,9].compute_and_differentiate(julian_date)
    return Pluto_position



def get_solar_vector(body_position,julian_date,kernel):
    sun_position        = get_sun_position_ICRF(kernel,julian_date)
    relative_position   = sun_position - body_position
    return relative_position


def get_position_ICRF(body,julian_date,kernel):
    match body:
        case "Sun":
            return get_earth_position_ICRF(kernel,julian_date)
        case "Mercury":
            return get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            return get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            return get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            return get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            return get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            return get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            return get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            return get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            return get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            return get_pluto_position_ICRF(kernel,julian_date)
    
def get_relative_position_ICRF(from_body,to_body,julian_date,kernel):
    match from_body:
        case "Sun":
            from_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Mercury":
            from_body_position = get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            from_body_position = get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            from_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            from_body_position = get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            from_body_position = get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            from_body_position = get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            from_body_position = get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            from_body_position = get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            from_body_position = get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            from_body_position = get_pluto_position_ICRF(kernel,julian_date)
        
    match to_body:
        case "Sun":
            to_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            to_body_position = get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            to_body_position = get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            to_body_position = get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            to_body_position = get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            to_body_position = get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            to_body_position = get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            to_body_position = get_pluto_position_ICRF(kernel,julian_date)
            
    #### Calculate relative position
    relative_position = to_body_position - from_body_position
    
    return relative_position

#  position of Mars with respect to the Earth takes three steps, from Mars to the Solar System barycenter to the Earth-Moon barycenter and finally to Earth itself
print('-----Mars wrt Earth-----')
position = kernel[0,4].compute(2457061.5)
position -= kernel[0,3].compute(2457061.5)
position -= kernel[3,399].compute(2457061.5)
print('Position (km):')
print(position)

# You can see that the output of this ephemeris DE421 is in kilometers

# Some ephemerides include velocity inline by returning a 6-vector instead of a 3-vector. For an ephemeris that does not, you can ask for the Chebyshev polynomial to be differentiated to produce a velocity, which is delivered as a second return value:

print('-----Mars wrt SS Barycenter -----')
position, velocity = kernel[0,4].compute_and_differentiate(2457061.5)
print('Position (km):')
print(position)
print('Velocity (km/day):')
print(velocity)
    
# The velocity will by default be distance traveled per day, in whatever units for distance the ephemeris happens to use. To get a velocity per second, simply divide by the number of seconds in a day:
print('Velocity (km/s):')
velocity_per_second = velocity / 86400.0
print(velocity_per_second)


#%% Plot Orbits of planets
print('------------------')
kernel = SPK.open(spk_filepath)


t1 = Time('2024-01-01 00:00:00', scale='utc')
t2 = Time('2024-12-21 00:00:00', scale='utc')

julian_date         = t2.jd
julian_date         = t2.jd
AU                  = 149597870.7

Sun_position        = kernel[0,10].compute(julian_date)
Mercury_position    = kernel[0,1].compute(julian_date)
Venus_position      = kernel[0,2].compute(julian_date)
Earth_position      = kernel[0,3].compute(julian_date)
Earth_position      -= kernel[3,399].compute(julian_date)
Mars_position       = kernel[0,4].compute(julian_date)
Jupiter_position    = kernel[0,5].compute(julian_date)
Saturn_position     = kernel[0,6].compute(julian_date)
Uranus_position     = kernel[0,7].compute(julian_date)
Neptune_position    = kernel[0,8].compute(julian_date)
Pluto_position      = kernel[0,9].compute(julian_date)

Sun     = np.array([[0,Sun_position[0]],      [0,Sun_position[1]],     [0,Sun_position[2]]])/AU
Mercury = np.array([[0,Mercury_position[0]],  [0,Mercury_position[1]], [0,Mercury_position[2]]])/AU
Venus   = np.array([[0,Venus_position[0]],    [0,Venus_position[1]],   [0,Venus_position[2]]])/AU
Earth   = np.array([[0,Earth_position[0]],    [0,Earth_position[1]],   [0,Earth_position[2]]])/AU
Mars    = np.array([[0,Mars_position[0]],     [0,Mars_position[1]],    [0,Mars_position[2]]])/AU
Jupiter = np.array([[0,Jupiter_position[0]],  [0,Jupiter_position[1]], [0,Jupiter_position[2]]])/AU
Saturn  = np.array([[0,Saturn_position[0]],   [0,Saturn_position[1]],  [0,Saturn_position[2]]])/AU
Uranus  = np.array([[0,Uranus_position[0]],   [0,Uranus_position[1]],  [0,Uranus_position[2]]])/AU
Neptune = np.array([[0,Neptune_position[0]],  [0,Neptune_position[1]], [0,Neptune_position[2]]])/AU
Pluto   = np.array([[0,Pluto_position[0]],    [0,Pluto_position[1]],   [0,Pluto_position[2]]])/AU



julian_date         = np.arange(t1.jd,t2.jd,1)

Sun_position        = kernel[0,10].compute(julian_date)/AU
Mercury_position    = kernel[0,1].compute(julian_date)/AU
Venus_position      = kernel[0,2].compute(julian_date)/AU
Earth_position      = kernel[0,3].compute(julian_date)
Earth_position      -= kernel[3,399].compute(julian_date)
Earth_position      = Earth_position/AU
Mars_position       = kernel[0,4].compute(julian_date)/AU
Jupiter_position    = kernel[0,5].compute(julian_date)/AU
Saturn_position     = kernel[0,6].compute(julian_date)/AU
Uranus_position     = kernel[0,7].compute(julian_date)/AU
Neptune_position    = kernel[0,8].compute(julian_date)/AU
Pluto_position      = kernel[0,9].compute(julian_date)/AU

fig = plt.figure()
ax  = fig.add_subplot(projection='3d')
ax.scatter(Sun[0], Sun[1], Sun[2],c='y')
ax.plot(Sun[0], Sun[1], Sun[2],label='Sun',c='y')

ax.scatter(Mercury[0], Mercury[1], Mercury[2],c='black')
ax.plot(Mercury[0], Mercury[1], Mercury[2],label='Mercury',c='black')

ax.scatter(Venus[0], Venus[1], Venus[2],c='purple')
ax.plot(Venus[0], Venus[1], Venus[2],label='Venus',c='purple')

ax.scatter(Earth[0], Earth[1], Earth[2],c='g')
ax.plot(Earth[0], Earth[1], Earth[2],label='Earth',c='g')

ax.scatter(Mars[0], Mars[1], Mars[2],c='r')
ax.plot(Mars[0], Mars[1], Mars[2],label='Mars',c='r')

ax.scatter(Jupiter[0], Jupiter[1], Jupiter[2],c='brown')
ax.plot(Jupiter[0], Jupiter[1], Jupiter[2],label='Jupiter',c='brown')

ax.scatter(Saturn[0], Saturn[1], Saturn[2],c='orange')
ax.plot(Saturn[0], Saturn[1], Saturn[2],label='Saturn',c='orange')

ax.scatter(Neptune[0], Neptune[1], Neptune[2],c='blue')
ax.plot(Neptune[0], Neptune[1], Neptune[2],label='Neptune',c='blue')

ax.scatter(Uranus[0], Uranus[1], Uranus[2],c='cyan')
ax.plot(Uranus[0], Uranus[1], Uranus[2],label='Uranus',c='cyan')

ax.scatter(Pluto[0], Pluto[1], Pluto[2],c='grey')
ax.plot(Pluto[0], Pluto[1], Pluto[2],label='Pluto',c='grey')

ax.plot3D(Sun_position[0,:],Sun_position[1,:],Sun_position[2,:],color='y')
ax.plot3D(Mercury_position[0,:],Mercury_position[1,:],Mercury_position[2,:],color='black')
ax.plot3D(Venus_position[0,:],Venus_position[1,:],Venus_position[2,:],color='purple')
ax.plot3D(Earth_position[0,:],Earth_position[1,:],Earth_position[2,:],color='g')
ax.plot3D(Mars_position[0,:],Mars_position[1,:],Mars_position[2,:],color='r')
ax.plot3D(Jupiter_position[0,:],Jupiter_position[1,:],Jupiter_position[2,:],color='brown')
ax.plot3D(Saturn_position[0,:],Saturn_position[1,:],Saturn_position[2,:],color='orange')
ax.plot3D(Neptune_position[0,:],Neptune_position[1,:],Neptune_position[2,:],color='blue')
ax.plot3D(Uranus_position[0,:],Uranus_position[1,:],Uranus_position[2,:],color='cyan')
ax.plot3D(Pluto_position[0,:],Pluto_position[1,:],Pluto_position[2,:],color='grey')

ax.set_xlabel('X [AU]')
ax.set_ylabel('Y [AU]')
ax.set_zlabel('Z [AU]')
ax.auto_scale_xyz([-25, 25], [-25, 25], [-25, 25])
ax.legend()


R_Sun_to_Earth = Earth_position - Sun_position
print(R_Sun_to_Earth[:,-1]*AU)
R_Sun_to_Earth = np.linalg.norm(R_Sun_to_Earth[:,-1],axis = 0)

print('Distance '+str(R_Sun_to_Earth*AU))

print(Earth_position[:,-1]*AU)
Earth_position = np.linalg.norm(Earth_position[:,-1],axis = 0)
print('Distance '+str(Earth_position *AU))


print('------------------')
#%% Plot Orbits of planets
kernel              = SPK.open(spk_filepath)
AU                  = 149597870.7*1

t1 = Time('2024-01-01 00:00:00', scale='utc')
t2 = Time('2024-12-21 00:00:00', scale='utc')

julian_date         = t2.jd
julian_date         = t2.jd
AU                  = 149597870.7

Sun_position        = kernel[0,10].compute(julian_date)
Earth_position      = kernel[0,3].compute(julian_date)
Earth_position      -= kernel[3,399].compute(julian_date)

Sun     = np.array([[0,Sun_position[0]],      [0,Sun_position[1]],     [0,Sun_position[2]]])
Earth   = np.array([[0,Earth_position[0]],    [0,Earth_position[1]],   [0,Earth_position[2]]])

julian_date         = np.arange(t1.jd,t2.jd,1)

Sun_position        = kernel[0,10].compute(julian_date)
Earth_position      = kernel[0,3].compute(julian_date)
Earth_position      -= kernel[3,399].compute(julian_date)
Earth_position      = Earth_position


fig = plt.figure()
ax  = fig.add_subplot(projection='3d')
ax.scatter(Sun[0], Sun[1], Sun[2],c='y')
ax.plot(Sun[0], Sun[1], Sun[2],label='Sun',c='y')

ax.scatter(Earth[0], Earth[1], Earth[2],c='g')
ax.plot(Earth[0], Earth[1], Earth[2],label='Earth',c='g')

ax.plot3D(Sun_position[0,:],Sun_position[1,:],Sun_position[2,:],color='y')
ax.plot3D(Earth_position[0,:],Earth_position[1,:],Earth_position[2,:],color='g')

ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')
ax.auto_scale_xyz([-1*AU, 1*AU], [-1*AU, 1*AU], [-1*AU, 1*AU])
ax.legend()

R_Sun_to_Earth = Earth_position - Sun_position
R_Sun_to_Earth = np.linalg.norm(R_Sun_to_Earth,axis = 0)
R_Sun_to_Earth_AU = R_Sun_to_Earth/AU

print('Aphelion: '+str(max(R_Sun_to_Earth)))
print('Perihelion '+str(min(R_Sun_to_Earth)))
print('Aphelion: '+str(max(R_Sun_to_Earth_AU)))
print('Perinelion: '+str(min(R_Sun_to_Earth_AU)))




