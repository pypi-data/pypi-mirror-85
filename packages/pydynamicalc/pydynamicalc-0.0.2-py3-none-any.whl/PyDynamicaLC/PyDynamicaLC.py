import os
from pylab import *
from PyAstronomy.modelSuite import forTrans as ft
from PyAstronomy import funcFit as fuf
from ttvfaster import run_ttvfaster
import scipy

####### INPUT #######
## Integration_Params:
    # t_min = t0 of integration [days]
    # t_max = integration limit [days]
    # dt = n-body sampling frequency [days^-1]

## Paths:
    # dyn_path: Path to TTVFast folder (should end with c_version/)
    # dyn_path_OS: Same path as dyn_path, except that it should be compatible with OS
    # dyn_file_name: Desired name of file

## Phot_Params: PHOTOMETRIC PARAMETERS
    # LC_times: list of times for which the lightcurve will be sampled [days]
    # LDcoeff1: linear limb-darkening coefficient
    # LDcoeff2: quadratic limb-darkening coefficient
    # r = numpy array of relative planet radii [R_star]
    # PlanetFlux: numpy array of additional fluxes from the planets (should be 0?)
    # transit_width: upper limit of the transit width relative to the orbital period

## Dyn_Params: DYNAMICAL PARAMETERS
    # LC_mode: string specifying which mode of lightcurve generation to use. Can be osc, ecc and circ (osculating, eccentric and circular, respectively)
    # m_star: stellar mass [m_sun]
    # r_star: stellar radius [r_sun]
    # masses: vector of planetary masses [m_earth]

    ### OSCULATING LIGHTCURVE - Keplerian parameters are initial conditions ###
    # dyn_coords: for LC_mode = osc, the initial conditions input can be input as either Keplerian or a Cartesian state vector, can be keplerian and cartesian
    # p: vector of planetary orbital periods at t_min [days]
    # incs: vector of planetary inclinations at t_min [deg]
    # Omegas: vector of planetary inclinations at t_min [deg]
    # ecosomega: vector of planetary ecos(omega)s at t_min [deg]
    # esinomega: vector of planetary esin(omega)s at t_min [deg]
    # tmids: vector of first times of mid-transit for each planet [days]

    ### ECCENTRIC/CIRCULAR LIGHTCURVE - Keplerian parameters are AVERAGE values ###
    # dyn_coords: for LC_mode = osc, the initial conditions input can be input as either Keplerian or a Cartesian state vector, can be keplerian and cartesian
    # p: vector of average planetary orbital periods [days]
    # incs: vector of average planetary inclinations [deg]
    # Omegas: vector of average planetary longitudes of ascending node [deg]
    # ecosomega: vector of average planetary ecos(omega)s [deg]
    # esinomega: vector of average planetary esin(omega)s [deg]
    # tmids: a mean reference epoch (i.e. the constant term in the linear fit to the times of transit)

#### Constants ####
earth_mass = 5.9736e24 # Earth_mass [kg]
m_sun = 1.988415860572226e30 # Solar mass [kg]
Mearth2Msol = earth_mass / m_sun
r_earth = 6371e3 # Earth radius [m]
r_sun = 6957e5 # Solar radius [m]
dayToSec = 86400.
m_to_AU = 1. / 149597870700.
Rsun_to_AU = r_sun * m_to_AU
sec_to_days = 1. / dayToSec
solar_radius_AU = r_sun * m_to_AU
K2 = 2.959122082855911e-4 # Gaussian gravitational constant squared (used by Mercury)
G_si = (K2 * ((1. / m_to_AU) ** 3)) / (m_sun * (dayToSec ** 2))
E_tol = 1e-15 * dayToSec # Eccentric Anomaly function tolerance

### Find nearest value to input value in the input array ####
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#### Running TTVFast through terminal (C) using state vector as initial conditions ####
def run_TTVFast_C_cartesian(positions_vec, velocities_vec, t_min, t_max, dt, file_name, stellar_mass, mass_vec, TTVFast_file_path, TTVFast_file_path_OS, Coords_output_fileName):

    nPl = len(mass_vec)

    f = open(TTVFast_file_path + "{0}.in.cartesian".format(file_name),"w")
    f.write(str(K2) + " \n")
    f.write(str(stellar_mass) + " \n")
    for i in range(nPl):
        f.write(str(mass_vec[i] * Mearth2Msol) + " \n")
        f.write('{0} {1} {2}'.format(positions_vec[i][0], positions_vec[i][1], -positions_vec[i][2]) + " \n")
        f.write('{0} {1} {2}'.format(velocities_vec[i][0], velocities_vec[i][1], -velocities_vec[i][2]) + " \n")
    f.close()

    f = open(TTVFast_file_path + "{0}_setup_cartesian.txt".format(file_name), "w")
    f.write('{0}.in.cartesian \n'.format(file_name))
    f.write('{0} \n'.format(t_min))
    f.write('{0} \n'.format(dt))
    f.write('{0} \n'.format(t_max))
    f.write('{0} \n'.format(nPl))
    f.write('{0} \n'.format(2))
    f.write('{0} \n'.format(Coords_output_fileName))
    f.close()

    os.system("cd ~ \n cd {0} \n rm {2} \n ./run_TTVFast {1}_setup_cartesian.txt Times_cartesian_new_{1} RV_file RV_out".format(TTVFast_file_path_OS, file_name, Coords_output_fileName))
    # os.system("cd ~ \n cd {0} \n ./run_TTVFast {1}_setup_cartesian.txt Times_cartesian_new_{1} RV_file RV_out".format(TTVFast_file_path_OS, file_name, Coords_output_fileName))

    Times_new = transpose(np.loadtxt(TTVFast_file_path + "Times_cartesian_new_{0}".format(file_name)))

    r_sky = []
    v_sky = []
    TTVFast_C_times = []
    TTVFast_C_TTVs = []
    P_model = []
    lin_eph= []

    for i in range(nPl):
        idx = np.where(Times_new[0] == i)[0]

        r_sky.append(Times_new[3][idx])
        v_sky.append(Times_new[4][idx])
        TTVFast_C_times.append(Times_new[2][idx])

        a = np.linspace(0, len(TTVFast_C_times[i]) - 1, len(TTVFast_C_times[i]))
        linear_fit = np.polyfit(a, TTVFast_C_times[i], 1)
        linear_ephemeris = linear_fit[1] + linear_fit[0] * a  # Polyfitting TTVFaster data to extract linear ephemeris for planet 0
        TTVFast_C_TTVs.append((TTVFast_C_times[i] - linear_ephemeris))
        P_model.append(linear_fit[0])
        lin_eph.append(linear_ephemeris)

    return TTVFast_C_times, TTVFast_C_TTVs, P_model, lin_eph

#### Run pythonic TTVFaster ####
def TTVFaster_Signal_Generator_nPl(p_vec, T_vec, m_vec, i_vec, ex_vec, ey_vec, stellar_mass, t_max): # Running TTVFaster in an n_Planet scenario

    ################# Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal

    nPl = len(p_vec)  # Assessing number of planets
    params = [stellar_mass]

    for j in range(nPl):   # optional alternative: params=np.asarray(([a.transpose(), b.transpose(), c.transpose()]))

        params.append(m_vec[j])
        params.append(p_vec[j])
        params.append(ex_vec[j])
        params.append(i_vec[j])
        params.append(- np.pi / 2)
        params.append(ey_vec[j])
        params.append(T_vec[j])

    data_ttvfaster = (run_ttvfaster(nPl, params, 0, t_max, 10))  # Generating TTVFaster data [days]

    OC_list = []
    times_list = []
    lin_eph = []

    for j in range(nPl):

        linear_this = np.array([i for i in range(len(data_ttvfaster[j]))]) * p_vec[j] + T_vec[j]
        OC_this = data_ttvfaster[j] - linear_this

        OC_list.append(OC_this)
        times_list.append(data_ttvfaster[j])
        lin_eph.append(linear_this)

    return np.array(OC_list), np.array(times_list), np.array(lin_eph)

#### Keplerian elements to Cartesian state vector (x, y, z, u, v, w) #### a [AU], i, omega, Omega and nu [deg], E [rad]
def Keplerian2Cartesian(a, e, i, omega, Omega, theta, mu, E):

    i = i * np.pi / 180
    omega = omega * np.pi / 180
    Omega = Omega * np.pi / 180
    theta = theta * np.pi / 180

    n = (mu / (a ** 3)) ** 0.5

    # E = 2 * math.atan((((1 - e) / (1 + e)) ** 0.5) * math.tan(theta / 2))
    # M = E - e * math.sin(E)

    r_mag = a * (1 - e * math.cos(E))
    h_mag = ((1 - (e ** 2)) * (a * mu)) ** 0.5
    p = a * (1 - e ** 2)

    x = r_mag * (np.cos(Omega) * np.cos(omega + theta) - np.sin(Omega) * np.sin(omega + theta) * np.cos(i))
    y = r_mag * (np.sin(Omega) * np.cos(omega + theta) + np.cos(Omega) * np.sin(omega + theta) * np.cos(i))
    z = r_mag * (np.sin(i) * np.sin(omega + theta))

    xdot = (x * h_mag * e / (r_mag * p)) * np.sin(theta) - (h_mag / r_mag) * (
                np.cos(Omega) * np.sin(omega + theta) + np.sin(Omega) * np.cos(omega + theta) * np.cos(i))
    ydot = (y * h_mag * e / (r_mag * p)) * np.sin(theta) - (h_mag / r_mag) * (
                np.sin(Omega) * np.sin(omega + theta) - np.cos(Omega) * np.cos(omega + theta) * np.cos(i))
    zdot = (z * h_mag * e / (r_mag * p)) * np.sin(theta) + (h_mag / r_mag) * (np.sin(i) * np.cos(omega + theta))

    return x, y, z, xdot, ydot, zdot

#### Keplerian to Cartesian (Astrocentric and Barycentric) ####
def Init_Conds(stellar_radius, stellar_mass, nPl, per_list, masses, inc_list, dex_list, dey_list, Tmid_list, Omega_list, t_min):

    e_vec = np.zeros(nPl)  # Initial eccentricity (scalar)
    omega_vec = np.zeros(nPl)  # Initial argument of periapse [degrees]
    n_vec = np.zeros(nPl) # Mean anomaly
    a_vec = np.zeros(nPl) # Mean semi-major axis
    a_rStar_vec = np.zeros(nPl) # Mean semi-major axis [rStar]
    E_Tr_vec = np.zeros(nPl) # Eccentric anomaly
    E_t0_vec = np.zeros(nPl) # Eccentric anomaly AT t0
    nu_t0_vec = np.zeros(nPl) # True anomaly AT t0
    ma_t0_vec = np.zeros(nPl)  # Initial mean anomaly [degrees] AT t0
    nu_Tr_vec = np.zeros(nPl) # True anomaly at TRANSIT
    mu_vec = np.zeros(nPl) # G(M_star + m_pl) [AU^3 M_sun^-1 day^-1]
    ma_mid_vec = np.zeros(nPl) # Mean anomaly at mid-transit [rad]
    inc_from_b_vec = np.zeros(nPl) # Mean anomaly at mid-transit [rad]
    T_periapse_vec = np.zeros(nPl) # Time of periapse passage [days]

    #### State vector arrays ####
    positions_vec = []
    velocities_vec = []

    #### Array needed for Python TTVFast ####
    planets = []

    #### Setting initial orbital elements for all planets by solving Kepler's equation from each Tmid to t0.
    for i in range(nPl):

        n_vec[i] = (2 * pi) / per_list[i]
        a_vec[i] = ((((stellar_mass * m_sun + masses[i] * earth_mass) * G_si * (per_list[i] * 24 * 3600) ** 2) / (4 * pi ** 2)) ** (1 / 3)) # Keplerian semi-major axis [m]
        a_rStar_vec[i] = a_vec[i] / (stellar_radius * r_sun) # Semi-major axis [rStar]

        e_vec[i] = sqrt(dex_list[i] ** 2 + dey_list[i] ** 2) # Eccentricity of planet i
        omega_vec[i] = math.degrees(math.atan2(dey_list[i], dex_list[i]))  # Argument of periapse of planet i [deg]

        #### SOLVING FOR ECCENTRICITY F INNER PLANET AND DELTA IN ECCENTRICITY OF THE OUTER ONES ####
        # if i == 0:
        #     e_vec[i] = sqrt(dex_list[i] ** 2 + dey_list[i] ** 2)  # Eccentricity of planet 0
        #     omega_vec[i] = math.degrees(math.atan2(dey_list[i], dex_list[i]))  # Argument of periapse of planet 0 [deg]
        # else:
        #     e_vec[i] = sqrt((dex_list[i] + dex_list[i - 1]) ** 2 + (dey_list[i] + dey_list[i - 1]) ** 2)  # Eccentricity of planet i>0
        #     omega_vec[i] = math.degrees(math.atan2((dey_list[i] + dey_list[i - 1]), (dex_list[i] + dex_list[i - 1])))  # Argument of periapse of planet i>0 [deg]
        #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END #### END ####

        b_vec = np.array([((a_rStar_vec[i] * cos(deg2rad(inc_list[i]))) / (stellar_radius)) * ((1 - e_vec[i] ** 2) / (1 + e_vec[i] * sin(deg2rad(omega_vec[i])))) for i in range(nPl)]) # Impact paramter
        inc_from_b_vec[i] = rad2deg(arccos((b_vec[i] * (stellar_radius / a_rStar_vec[i])) * ((1 + e_vec[i] * sin(deg2rad(omega_vec[i]))) / (1 - e_vec[i] ** 2)))) # Inclination back from impact parameter

        #### Extracting M_mid from Kepler's equation ####
        nu_Tr_vec[i] = pi / 2 - deg2rad(omega_vec[i]) # True anomaly at mid-transit [rad]
        E_Tr_vec[i] = 2 * math.atan2(sqrt((1 - e_vec[i]) / (1 + e_vec[i])) * sin(nu_Tr_vec[i] / 2), cos(nu_Tr_vec[i] / 2)) # Eccentric anomaly at mid-transit [rad]
        ma_mid_vec[i] = E_Tr_vec[i] - e_vec[i] * sin(E_Tr_vec[i]) # Mean anomaly at mid-transit [rad]
        T_periapse_vec[i] = Tmid_list[i] - (ma_mid_vec[i] / n_vec[i]) # Time of periapse passage [days]

        ma_t0_vec[i] = (ma_mid_vec[i] - n_vec[i] * (Tmid_list[i] - t_min)) # Mean anomaly at t0 [rad]
        E_t0_vec[i] = calc_E(ma_t0_vec[i], e_vec[i], E_tol) % (2 * pi) # Eccentric anomaly at t0 [rad]

        nu_t0_vec[i] = 2 * math.atan2(sqrt((1 + e_vec[i]) / (1 - e_vec[i])) * sin(E_t0_vec[i] / 2), cos(E_t0_vec[i] / 2)) # True anomaly at t0 [rad]

        mu_vec[i] = K2 * (stellar_mass + masses[i] * Mearth2Msol) # G * (M_star + sum(m_planet)) [AU, Msol, day]

        #### Transforming orbital parameters to XYZ, UVW state vector #### FUNCTION 1
        x, y, z, vx, vy, vz = Keplerian2Cartesian(a_vec[i] * m_to_AU, e_vec[i], inc_list[i], omega_vec[i], Omega_list[i], rad2deg(nu_t0_vec[i]) % 360, mu_vec[i], E_t0_vec[i]) # Cartesian state-vector [AU, AU day^-1]
        positions_vec.append([x, y, -z])
        velocities_vec.append([vx, vy, -vz])

    #### Extracting barycentric state vector for use of fortran ####
    bary_positions_vec, bary_velocities_vec, bary_star_xyz, bary_star_uvw = Astrocentric2Barycentric(np.array(positions_vec), np.array(velocities_vec), stellar_mass, np.array(masses))

    output = {"planets": planets, "xyz_astro": positions_vec, "uvw_astro": velocities_vec, "xyz_bary": bary_positions_vec, "uvw_bary": bary_velocities_vec, "star_xyz": bary_star_xyz, "star_uvw": bary_star_uvw, "n": n_vec, "a_m": a_vec, "a_rStar": a_rStar_vec, "e": e_vec, "omega": omega_vec, \
              "nu_Tr": nu_Tr_vec, "E_Tr": E_Tr_vec, "ma_Tr": ma_mid_vec, "ma_t0": ma_t0_vec, "E_t0": E_t0_vec, "nu_t0": nu_t0_vec, "mu": mu_vec, "inc_from_b": inc_from_b_vec, "b": b_vec}

    return output

#### taken from Http://ccar.colorado.edu/asen5070/Handouts/cart2kep2002.pdf ###
def Cartesian2Keplerian(positions, velocities, mu, mass, stellar_mass):

    H = np.cross(positions, velocities)
    h = np.linalg.norm(H,2)
    r = np.linalg.norm(positions, 2)
    v = np.linalg.norm(velocities, 2)

    ### Calculate specific energy
    E = ((v ** 2) / 2) - (mu / r)

    ### Calculate semi-major axis
    a = - mu / (2 * E)

    ### Calculate eccentricity
    e = (1 - ((h ** 2) / (a * mu))) ** 0.5

    if isreal(e) == False:
        e = real(e)

    ### Calculate inclination
    inc = arccos(H[2] / h)

    ### Calculate Longitude of Ascending node
    Omega = math.atan2(H[0], -H[1])

    ### Argument of latitutde u = w + f
    if inc != 0:
        u = math.atan2(positions[2], sin(inc)* (positions[0]*cos(Omega) + positions[1] * sin(Omega)))
    else:
        u = math.atan2(positions[1], positions[0] - Omega)

    ### Semi-latus rectum
    p = a * (1 - (e ** 2))

    ### True anomaly
    f = math.atan2(sqrt(p / mu) * dot(positions, velocities), p - r)

    ### Eccentric anomaly
    EA = 2 * math.atan2(sqrt((1 - e) / (1 + e)) * sin(f / 2), cos(f / 2))

    ### Argument of periapse
    omega = u - f

    ### Longitude of periapse
    Pomega = omega + Omega

    ### Mean motion
    n = sqrt(mu / (a ** 3))

    ### Time since periapse
    dT = (1/n) * ((EA - e * sin(EA)))

    ### Mean anomaly
    ma = n * dT

    per = 2 * pi * sqrt(((a / m_to_AU) ** 3) / (G_si * ((stellar_mass * m_sun) + (mass * Mearth2Msol * m_sun)))) * sec_to_days # Orbital period

    return a, e, inc, Omega, f, omega, ma, per

#### Convert Cartesian Astrocentric coordinates to Barycentric coordinates ####
def Astrocentric2Barycentric(positions, velocities, stellar_mass, planet_masses):

    nPl = len(planet_masses)

    planet_masses = planet_masses * Mearth2Msol

    X = np.array(sum([planet_masses[i] * positions[i][0] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))
    Y = np.array(sum([planet_masses[i] * positions[i][1] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))
    Z = np.array(sum([planet_masses[i] * positions[i][2] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))

    U = np.array(sum([planet_masses[i] * velocities[i][0] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))
    V = np.array(sum([planet_masses[i] * velocities[i][1] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))
    W = np.array(sum([planet_masses[i] * velocities[i][2] for i in range(nPl)])) / (stellar_mass + sum(planet_masses))

    V_star = np.array([U, V, W]) * -1 # Barycentric motion of the star
    R_star = np.array([X, Y, Z]) * -1 # Barycentric position of the star

    positions_bary = positions + R_star # Barycentric position of the planets
    velocities_bary = velocities + V_star # Barycentric motion of the planets

    return positions_bary, velocities_bary, R_star, V_star

#### Calculating True Anomaly given Mean Anomaly ####
def calc_E(M, e, EPS):

    thisE = M
    es = e * sin(thisE)
    EesM = thisE - es - M
    ec1 = 1 - e * cos(thisE)
    deltaE = - EesM * ec1 / (ec1 * ec1 - 0.5 * EesM * es)

    while abs(deltaE) > EPS:
        thisE = thisE + deltaE
        es = e * sin(thisE)
        EesM = thisE - es - M
        ec1 = 1 - e * cos(thisE)
        deltaE = - EesM * ec1 / (ec1 * ec1 - 0.5 * EesM * es)

    return thisE

#### Osculating parameters reader ####
def calc_osculating_OrbitalParams(mu_vec, masses, stellar_mass, TTVFast_Folder, Coords_output_fileName):

    #### Uploading the state vector at mid-transits for both planets to convert back to orbital elements ####
    cartesian_coords = transpose(np.loadtxt(TTVFast_Folder + Coords_output_fileName))

    nPl = len(masses)

    positions_nPl = []

    e_vec_nPl = []
    omega_vec_nPl = []
    nu_vec_nPl = []
    Omega_vec_nPl = []
    time_vec_nPl = []
    p_vec_nPl = []
    inc_vec_nPl = []
    a_vec_nPl = []

    for n in range(nPl):

        idx = np.where(cartesian_coords[-1] == n)[0]

        positions = []

        for j in range(len(cartesian_coords)):
            positions.append(cartesian_coords[j][idx])

        positions_nPl.append(positions)

        x_pl = cartesian_coords[0][idx]
        y_pl = cartesian_coords[1][idx]
        z_pl = cartesian_coords[2][idx]
        vx_pl = cartesian_coords[3][idx]
        vy_pl = cartesian_coords[4][idx]
        vz_pl = cartesian_coords[5][idx]
        time_output = cartesian_coords[6][idx]

        e_vec = np.zeros(len(idx))
        omega_vec = np.zeros(len(idx))
        nu_vec = np.zeros(len(idx))
        Omega_vec = np.zeros(len(idx))
        p_vec = np.zeros(len(idx))
        inc_vec = np.zeros(len(idx))
        a_vec = np.zeros(len(idx))

        for i in range(len(idx)):

            # this_positions = Vector3D(-z_pl[i], x_pl[i], y_pl[i])
            # this_velocities = Vector3D(-vz_pl[i], vx_pl[i], vy_pl[i])
            #
            # orb_new = orbitalElements(0, 0, 0, 0, 0, 0, this_positions, this_velocities, K2, stellar_mass)
            # orbital_elements = orb_new.calcOrbitFromVector()
            # orbital_elements = np.array([rad2deg(orbital_elements[0]), orbital_elements[1], rad2deg(orbital_elements[2]),rad2deg(orbital_elements[3])])
            #
            # omega_vec[i] = orbital_elements[0]
            # e_vec[i] = orbital_elements[1]
            # nu_vec[i] = orbital_elements[2]
            # Omega_vec[i] = orbital_elements[3] - 90 # Correction for TTVFast coordinate system
            #
            this_positions = [-z_pl[i], x_pl[i], y_pl[i]]
            this_velocities = [-vz_pl[i], vx_pl[i], vy_pl[i]]

            a, e, inc, Omega, f, omega, ma, p = Cartesian2Keplerian(this_positions, this_velocities, mu_vec[n], masses[n], stellar_mass)

            omega_vec[i] = rad2deg(omega)
            e_vec[i] = e
            nu_vec[i] = rad2deg(f)
            Omega_vec[i] = rad2deg(Omega) - 90
            p_vec[i] = p
            inc_vec[i] = 90 - rad2deg(inc)
            a_vec[i] = a

        e_vec_nPl.append(e_vec)
        omega_vec_nPl.append(omega_vec)
        nu_vec_nPl.append(nu_vec)
        Omega_vec_nPl.append(Omega_vec)
        time_vec_nPl.append(time_output)
        p_vec_nPl.append(p_vec)
        inc_vec_nPl.append(inc_vec)
        a_vec_nPl.append(a_vec)

    return np.array(e_vec_nPl), np.array(omega_vec_nPl), np.array(Omega_vec_nPl), np.array(nu_vec_nPl), np.array(time_vec_nPl), np.array(p_vec_nPl), array(inc_vec_nPl), array(a_vec_nPl)

def maEcc_with_oversmpling(Time, per, p, a, i, linLimb, quadLimb, Omega, omega, e, tau, orbit="keplerian", ld="quad", b=0, ReBin_N=1, ReBin_dt=0):
        # Added ReBin_N, ReBin_dt to allow for finite integration time calculation by re-binning. These are the PyAstronomy parameters for the number of subsamples and the duration of the original samples

        if ReBin_N > 1 and ReBin_dt > 0:
            MA_Rebin = fuf.turnIntoRebin(ft.MandelAgolLC)
            ma = MA_Rebin(orbit="keplerian", ld="quad")
            ma.setRebinArray_Ndt(Time, ReBin_N, ReBin_dt)
        else:
            ma = ft.MandelAgolLC(orbit="keplerian", ld="quad")

        # ma.pars._Params__params={"orbit":orbit, "ld":ld, "per":per, "i":i, "a":a, "p":p, "linLimb":linLimb, "quadLimb":quadLimb, "b":b, "tau":tau, "e": e, "w": omega, "Omega":Omega}

        ma["per"] = per
        ma["i"] = i
        ma["a"] = a
        ma["p"] = p
        ma["linLimb"] = linLimb
        ma["quadLimb"] = quadLimb
        ma["b"] = b
        ma["Omega"] = Omega
        ma["w"] = omega
        ma["e"] = e
        ma["tau"] = tau
        model = ma.evaluate(Time)

        return model

#### Eccentric (constant) light-curve with TTVs ####
def TTV_ecc_LC(time, TTV_signal, TT0, TTV_times, p, a, inc, b, linLimb_coefficient, quadLimb_coefficient, planet_star_ratio, Omega, omega, e, transit_width, ReBin_N=1, ReBin_dt=0):

    ma_ttv = np.ones(len(time))

    i_transits = [int(i) for i in range(len(time)) if abs(((time[i] - TT0 + (p / 2)) % p) - (p / 2)) < p * transit_width] # Indices of transists for the entire light curve
    t_transits = time[i_transits] # Times of transits for the entire light curve
    j_transits = t_transits // p # Index of each transit event assigned assigned to relevant indices of each transit

    #### Solving Kepler's equation for each time of mid-transit in order to generate initial condition Keplerian parameters for each individual transit, given its osculating values (omega, Omega, nu, Tmid)
    n = (2 * pi) / p
    nu_Tr = pi / 2 - deg2rad(omega)

    E_Tr = np.array(2 * math.atan2(sqrt((1 - e) / (1 + e)) * sin(nu_Tr / 2), cos(nu_Tr / 2)))
    ma_mid = np.array(E_Tr - e * sin(E_Tr))
    T_periapse_vec = TTV_times - (ma_mid / n)  # Time of periapse passage [days]

    i_transits = [int(i) for i in range(len(time)) if abs(((time[i] - TT0 + (p / 2)) % p) - (p / 2)) < p * transit_width] # Indices of transists for the entire light curve
    t_transits = time[i_transits] # Times of transits for the entire light curve
    j_transits = t_transits // p # Index of each transit event assigned assigned to relevant indices of each transit

    TTV_signal = np.array(TTV_signal)
    shifted_times = t_transits

    j_indices = ((t_transits - TT0 + p / 2) // p)
    j_indices = np.array([int(i) for i in j_indices])

    for i in range(len(shifted_times)):
        nearest_TTV_idx = np.where(TTV_times == find_nearest(TTV_times, shifted_times[i]))[0]
        shifted_times[i] = shifted_times[i] - TTV_signal[nearest_TTV_idx]

    ma_transits = maEcc_with_oversmpling(Time=shifted_times, per=p, p=planet_star_ratio, a=a, i=inc, linLimb=linLimb_coefficient, quadLimb=quadLimb_coefficient, Omega = Omega, omega = omega + 180, e = e, tau = T_periapse_vec[0], orbit="keplerian", ld="quad", b=b, ReBin_N=ReBin_N, ReBin_dt=ReBin_dt)
    ma_ttv[i_transits] = ma_transits

    return ma_ttv

#### Osculating light-curve ####
def TTV_osculating_LC(time, TTV_times, b, linLimb_coefficient, quadLimb_coefficient, planet_star_ratio, Omega_vec, omega_vec, e_vec, p_vec, inc_vec, a_vec, transit_width=0.05, ReBin_N=1, ReBin_dt=0):

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    ma_ttv = np.ones(len(time))

    if len(TTV_times) != len(e_vec):
        print("Length of TTV and osculating parameter vectors is not equal.")
    else:

        TT0 = TTV_times[0]
        p = p_vec[0]

        i_transits = np.array([int(i) for i in range(len(time)) if abs(((time[i] - TT0 + (p / 2)) % p) - (p / 2)) < p * transit_width]) # Indices of transists for the entire light curve
        t_transits = time[i_transits] # Times of transits for the entire light curve
        j_transits = t_transits // p # Index of each transit event assigned assigned to relevant indices of each transit
        j_transits -= j_transits[0]
        j_transits_idxs = np.unique(j_transits)

        #### Solving Kepler's equation for each time of mid-transit in order to generate initial condition Keplerian parameters for each individual transit, given its osculating values (omega, Omega, nu, Tmid)
        n = (2 * pi) / p_vec
        nu_Tr_vec = pi / 2 - deg2rad(omega_vec)

        E_Tr_vec = np.array([2 * math.atan2(sqrt((1 - e_vec[i]) / (1 + e_vec[i])) * sin(nu_Tr_vec[i] / 2), cos(nu_Tr_vec[i] / 2)) for i in range(len(e_vec))])
        ma_mid_vec = np.array([E_Tr_vec[i] - e_vec[i] * sin(E_Tr_vec[i]) for i in range(len(E_Tr_vec))])
        T_periapse_vec = TTV_times - (ma_mid_vec / n)  # Time of periapse passage [days]

        shifted_times = t_transits

        for i in range(len(j_transits_idxs)):

            transit_idxs = np.where(j_transits == j_transits_idxs[i])[0]
            nearest_TTV_idx = np.where(TTV_times == find_nearest(TTV_times, average(shifted_times[transit_idxs])))[0][0]

            ma_transits = maEcc_with_oversmpling(Time = shifted_times[transit_idxs], per = p_vec[nearest_TTV_idx], p=planet_star_ratio, a=a_vec[nearest_TTV_idx], i = inc_vec[nearest_TTV_idx],linLimb=linLimb_coefficient, quadLimb=quadLimb_coefficient,Omega = Omega_vec[nearest_TTV_idx], omega = omega_vec[nearest_TTV_idx] + 180, e = e_vec[nearest_TTV_idx], tau = T_periapse_vec[nearest_TTV_idx], orbit="keplerian", ld="quad",b=b, ReBin_N=ReBin_N, ReBin_dt=ReBin_dt)
            ma_ttv[i_transits[transit_idxs]] = ma_transits
            min_LC_idx = np.where(ma_transits == min(ma_transits))[0][0] # For debugging

        return ma_ttv

#### Circular light-curve with TTVs ####
def TTV_circ_LC(time, TTV_signal, times, TT0, p, a, inc, b, linLimb_coefficient, quadLimb_coefficient, planet_star_ratio, transit_width, ReBin_N=1, ReBin_dt=0):

    def ma_with_oversmpling(Time, per, Tmid, p, a, i, linLimb, quadLimb, orbit="circular", ld="quad", b=0, ReBin_N=1, ReBin_dt=0, ToPlot=False):
        # Added ReBin_N, ReBin_dt to allow for finite integration time calculation by re-binning. These are the PyAstronomy parameters for the number of subsamples and the duration of the original samples

            if ReBin_N>1 and ReBin_dt>0:
                MA_Rebin = fuf.turnIntoRebin(ft.MandelAgolLC)
                ma = MA_Rebin()
                ma.setRebinArray_Ndt(Time, ReBin_N, ReBin_dt)
            else:
                ma = ft.MandelAgolLC()

            ma.pars._Params__params={"orbit":orbit, "ld":ld, "per":per, "i":i, "a":a, "p":p, "linLimb":linLimb, "quadLimb":quadLimb, "b":b, "T0":Tmid}
            model= ma.evaluate(Time)

            if ToPlot:
                plt.plot((Time - Tmid + per/2) % per - per/2, model, '.')
                plt.xlabel("Time since T_mid [d]")
                #plt.show()
            return model

    ma_ttv = np.ones(len(time))

    i_transits = [int(i) for i in range(len(time)) if abs(((time[i] - TT0 + (p / 2)) % p) - (p / 2)) < p * transit_width] # Indices of transists for the entire light curve
    t_transits = time[i_transits] # Times of transits for the entire light curve
    j_transits = t_transits // p # Index of each transit event assigned assigned to relevant indices of each transit

    TTV_signal = np.array(TTV_signal)
    shifted_times = t_transits

    j_indices = ((t_transits - TT0 + p / 2) // p)
    j_indices = np.array([int(i) for i in j_indices])

    for i in range(len(shifted_times)):
        nearest_TTV_idx = np.where(times == find_nearest(times, shifted_times[i]))[0]
        shifted_times[i] = shifted_times[i] - TTV_signal[nearest_TTV_idx]

    ma_transits = ma_with_oversmpling(Time=shifted_times, per=p, Tmid=TT0, p=planet_star_ratio, a=a, i=inc, linLimb=linLimb_coefficient, quadLimb=quadLimb_coefficient, orbit="circular", ld="quad", b=b, ReBin_N=ReBin_N, ReBin_dt=ReBin_dt, ToPlot=False)
    ma_ttv[i_transits] = ma_transits

    return ma_ttv

#### Light-curve Generator ####
def LightCurve_Gen(Dyn_Params, Phot_Params, Integration_Params, Paths, verbose):

    #### INTEGRATION PARAMETERS ####
    t_min, t_max, dt = Integration_Params["t_min"], Integration_Params["t_max"], Integration_Params["dt"] # Integration params - start time, end time and sampling (dt should be < p0_inner / 20) [days]
    stellar_mass, stellar_radius = Dyn_Params["m_star"], Dyn_Params["r_star"] # Stellar mass and stellar radius [msun], [rsun], respectively.

    #### DYNAMICAL PARAMETERS
    planet_masses = np.array(Dyn_Params["masses"]) # Planetary masses [mEarth]
    nPl = len(planet_masses)

    if verbose == True:
        print("PyDynamicaLC initialized with the following parameters: \n")
        print("Integrations parameters: from {0} to {1} [days] with dt = {2}".format(t_min, t_max, dt))
        print("Stellar parameters: {0} [m_sun], {1} [r_sun]".format(stellar_mass, stellar_radius))
        print("{0} planets of masses: {1} [m_earth] \n".format(len(planet_masses), planet_masses))

    #### PHOTOMETRIC PARAMETERS
    LC_times = Phot_Params["LC_times"]
    MAmodels = np.zeros((nPl, len(LC_times)))

    #### Generating output dictionary ####
    output = {}

    #### Generating lightcurve using osculating Keplerian parameters ####
    if Dyn_Params["LC_mode"] == "osc":

        if verbose == True:
            print("Lightcurve mode: osculating (TTVFast).")

        #### PATHS ####
        TTVFast_path, TTVFast_path_OS, file_name, Coords_output_fileName = Paths["dyn_path"], Paths["dyn_path_OS"], Paths["dyn_fileName"], Paths["Coords_output_fileName"] # Path to the TTVFast folder, regular and OS for terminal execution.

        #### Dynamical params input - turn into cartesian ####
        if Dyn_Params["dyn_coords"] == "keplerian":

            if verbose == True:
                print("Input initial conditions for TTVFast in Keplerian form.")

            # print("Generating osculating lightcurve with Keplerian initial conditions.")

            per_list = np.array(Dyn_Params["p"])  # Orbital periods of the planets at t0
            inc_list = np.array(Dyn_Params["incs"])  # Inclinations of the planets at t0
            ex_list = np.array(Dyn_Params["ecosomega"])  # e_x of the planets at t0
            ey_list = np.array(Dyn_Params["esinomega"])  # e_y  of the planets at t0
            tmid_list = np.array(Dyn_Params["tmids"])  # First time of mid-transit of the planets
            Omega_list = np.array(Dyn_Params["Omegas"] ) # Omegas of the planets at t0

            # Converting Keplerian elements to Cartesian state vectors (x, y, z, x_dot, y_dot, z_dot)
            Kep2Cart_output = Init_Conds(stellar_radius, stellar_mass, nPl, per_list, planet_masses, inc_list, ex_list, ey_list, tmid_list, Omega_list, t_min)

            positions_vec = Kep2Cart_output["xyz_astro"]
            velocities_vec = Kep2Cart_output["uvw_astro"]

        elif Dyn_Params["dyn_coords"] == "cartesian":

            if verbose == True:
                print("Input initial conditions for TTVFast in Cartesian form. Make sure that the z and z_dot coordinates are with an opposite sign.")

            positions_vec, velocities_vec = Dyn_Params["xyz"], Dyn_Params["uvw"]
        else:
            print("dyn_mode can either be keplerian or cartesian. Terminating.")
            exit()

        #### Simulating dynamics using TTVFast ####
        times, TTVs, P_model, lin_eph = run_TTVFast_C_cartesian(positions_vec, velocities_vec, t_min, t_max, dt, file_name, stellar_mass, planet_masses, TTVFast_path, TTVFast_path_OS, Coords_output_fileName)

        #### Extracting osculating parameters ####
        mu_vec = np.array([K2 * (stellar_mass + planet_masses[i] * Mearth2Msol) for i in range(len(planet_masses))])# G * (M_star + sum(m_planet)) [AU, Msol, day]
        e_osc, omega_osc, Omega_osc, nu_osc, times_osc, p_osc, inc_osc, a_AU_osc = calc_osculating_OrbitalParams(mu_vec, planet_masses, stellar_mass, TTVFast_path, Coords_output_fileName) # Uplaod osculating parameters from TTVFast_C
        a_osc = a_AU_osc / (stellar_radius * r_sun * m_to_AU) # Normalize osculating semi-major axis from AU to r_star

        # Adding osculating parameter vectors to the output dictionary #
        output["e_osc"], output["omega_osc"], output["Omega_osc"], output["nu_osc"], output["p_osc"], output["inc_osc"], output["a_AU_osc"], output["aOverR_osc"] = e_osc, omega_osc, Omega_osc, nu_osc, p_osc, inc_osc, a_AU_osc, a_osc

        if verbose == True:
            print("Adding vectors of osculating Keplerian parameters to the output dictionary. \n")

        MAmodels = np.zeros((nPl, len(LC_times)))

        #### Generating lightcurve ####
        for i in range(nPl):
            MAmodels[i, :] = TTV_osculating_LC(LC_times, times[i], Phot_Params["PlanetFlux"][i], Phot_Params["LDcoeff1"], Phot_Params["LDcoeff2"], Phot_Params["r"][i], Omega_osc[i], omega_osc[i], e_osc[i], p_osc[i], inc_osc[i], a_osc[i], Phot_Params["transit_width"], Phot_Params["ReBin_N"], Phot_Params["ReBin_dt"])
    #### Generating lightcurve using average Keplerian parameters and average eccentricity to shape the transit curve ####
    elif Dyn_Params["LC_mode"] == "ecc":

        if verbose == True:
            print("Lightcurve mode: eccentric (TTVFaster). \n")

        per_list = Dyn_Params["p"]  # Average orbital periods
        a_list = Dyn_Params["a"]  # semimajor axes [AU]
        inc_list = Dyn_Params["incs"]  # Average inclinations
        ex_list = Dyn_Params["ecosomega"]  # e_x of the planets
        ey_list = Dyn_Params["esinomega"]  # e_y  of the planets
        tmid_list = Dyn_Params["tmids"]  # First time of mid-transit of the planets
        Omega_list = Dyn_Params["Omegas"]  # Average Omegas of the planets
        tmid_list = np.array([tmid_list[i] - (((tmid_list[i] - t_min) // per_list[i]) * per_list[i]) for i in range(nPl)], dtype = float) # Shifting the first linear ephemeris by an amount Pbar to the closest transit to t_min

        e_list = np.zeros(nPl)  # Initial eccentricity (scalar)
        omega_list = np.zeros(nPl)  # Initial argument of periapse [degrees]

        #### Generate TTVFaster times and TTVs ####
        TTVs, times, lin_eph = TTVFaster_Signal_Generator_nPl(per_list, tmid_list, planet_masses * Mearth2Msol, inc_list, ex_list, ey_list, stellar_mass, t_max - t_min)

        for i in range(nPl):

            e_list[i] = sqrt(ex_list[i] ** 2 + ey_list[i] ** 2)  # Eccentricity of planet 0
            omega_list[i] = math.degrees(math.atan2(ey_list[i], ex_list[i]))  # Argument of periapse of planet 0 [deg]

            MAmodels[i, :] = TTV_ecc_LC(LC_times, TTVs[i], times[i][0], times[i], per_list[i], a_list[i],
                                        inc_list[i], Phot_Params["PlanetFlux"][i], Phot_Params["LDcoeff1"], Phot_Params["LDcoeff2"], Phot_Params["r"][i], Omega_list[i], omega_list[i],
                                        e_list[i], Phot_Params["transit_width"], Phot_Params["ReBin_N"], Phot_Params["ReBin_dt"])
    #### Generating lightcurve using average Keplerian parameters and circular orbit shape of the transit curve ####
    elif Dyn_Params["LC_mode"] == "circ":

        if verbose == True:
            print("Lightcurve mode: quasi-circular (TTVFaster). \n")

        per_list = Dyn_Params["p"]  # Average orbital periods
        a_list = Dyn_Params["a"]  # semimajor axes [AU]
        inc_list = Dyn_Params["incs"]  # Average inclinations
        ex_list = Dyn_Params["ecosomega"]  # e_x of the planets
        ey_list = Dyn_Params["esinomega"]  # e_y  of the planets
        tmid_list = Dyn_Params["tmids"]  # First time of mid-transit of the planets
        tmid_list = np.array([tmid_list[i] - (((tmid_list[i] - t_min) // per_list[i]) * per_list[i]) for i in range(nPl)], dtype = float) # Shifting the first linear ephemeris by an amount Pbar to the closest transit to t_min

        #### Generate TTVFaster times and TTVs ####
        TTVs, times, lin_eph = TTVFaster_Signal_Generator_nPl(per_list, tmid_list, planet_masses * Mearth2Msol, inc_list, ex_list, ey_list, stellar_mass, t_max - t_min)

        for i in range(nPl):
            MAmodels[i, :] = TTV_circ_LC(LC_times, TTVs[i], times[i], tmid_list[i], per_list[i], a_list[i],
                                             inc_list[i], Phot_Params["PlanetFlux"][i], Phot_Params["LDcoeff1"], Phot_Params["LDcoeff2"], Phot_Params["r"][i],
                                             Phot_Params["transit_width"], Phot_Params["ReBin_N"], Phot_Params["ReBin_dt"])
    else:
        print("LC_mode can only be one of three: osc (for osculating), ecc (for eccentric) or circ (for quasi-circular). Terminating.")
        exit()

    # Combining all single-planet transit lightcurves into a multi-planet lightcurve #
    lightcurve = (MAmodels.sum(axis=0) - nPl + 1)

    # Populating output dictionary with the resulting TTVFast timing, TTVs, linear ephemeris vector and the multi-planet and single-planet lightcurves #
    output["times"], output["ttvs"], output["lin_eph"], output["lightcurve_allPlanets"], output["lightcurve_singlePlanets"] = times, TTVs, lin_eph, lightcurve, MAmodels

    return output

#### MultiNest fitter ####
def run_multinest(params, Dyn_Params, Phot_Params, Integration_Params, Paths):

    import pymultinest

    #### Optimizing masses and eccentricity differences using TTVFaster (3 degrees of freedom per planet) ####
    if params["mode"] == "TTVFaster":

        if Dyn_Params["LC_mode"] != "ecc" and Dyn_Params["LC_mode"] != "circ":
            print("Dyn_Params[LC_mode] can only be either ecc or circ. Exiting.")
            exit()

        if params["verbose"] == True:
            print("Optimizing delta_ex, delta_ey and mass for {0} planets with TTVFaster. \n".format(params["nPl"]))

        nDim, nPar = 3 * params["nPl"], 3 * params["nPl"]

        mass_prior = params["mass_prior"][0]
        ex_prior = params["ex_prior"][0]
        ey_prior = params["ey_prior"][0]

        if params["verbose"] == True:
            print("Chosen parameter priors are:")
            if ex_prior == "ray":
                print("ex: rayleigh distribution with scale-width of {0}".format(params["ex_prior"][1]))
            if ex_prior == "lin":
                print("ex: linear within the boundaries: {0}-{1}".format(params["ex_prior"][1], params["ex_prior"][2]))
            if ex_prior == "log":
                print("ex: logarithmic within the boundaries: 10^{0}, 10^{1}".format(params["ex_prior"][1], params["ex_prior"][2]))

            if ey_prior == "ray":
                print("ey: rayleigh distribution with scale-width of {0}".format(params["ey_prior"][1]))
            if ey_prior == "lin":
                print("ey: linear within the boundaries: {0}-{1}".format(params["ey_prior"][1], params["ey_prior"][2]))
            if ey_prior == "log":
                print("ey: logarithmic within the boundaries: 10^{0}, 10^{1}".format(params["ey_prior"][1], params["ey_prior"][2]))

            if mass_prior == "lin":
                print("mass: linear within the boundaries: {0}-{1} [m_earth]".format(params["mass_prior"][1], params["mass_prior"][2]))
            if mass_prior == "log":
                print("mass: logarithmic within the boundaries: 10^{0}, 10^{1} [m_earth]".format(params["mass_prior"][1], params["mass_prior"][2]))

            print("\n")

        #### Model function ####
        def model(mass, exd, eyd, nPl):

            #### Turning the delta_ex, delta_ey values into absolute eccentricity components
            ex = np.array([exd[0]] + [exd[0] + exd[i] for i in range(1, nPl)])
            ey = np.array([eyd[0]] + [eyd[0] + eyd[i] for i in range(1, nPl)])

            Dyn_Params["masses"] = mass
            Dyn_Params["ecosomega"] = ex
            Dyn_Params["esinomega"] = ey

            #### Generating model ####
            model = LightCurve_Gen(Dyn_Params, Phot_Params, Integration_Params, Paths, False)["lightcurve_allPlanets"]

            # plt.plot(params["data_LC"], 's', color = 'black')
            # plt.plot(model, color = 'orange')
            # plt.show()
            # exit()

            #### Calculating loglikelihood ####
            gaussian_loglike = - 0.5 * np.sum(np.log(2 * pi * params["data_LC_err"])) - 0.5 * np.sum(((params["data_LC"] - model) / params["data_LC_err"]) ** 2)  # Gaussian -2 * loglikelihood

            return gaussian_loglike

        #### Prior function ####
        def prior(cube, nDim, nPar):

            nPl = params["nPl"]

            # Mass prior
            for j in range(nPl):
                if params["mass_prior"][0] == "log":
                    cube[j] = 10 ** params["mass_prior"][1] + (10 ** params["mass_prior"][2] - 10 ** params["mass_prior"][1]) * cube[j]  # uniform distributon between massPrior(2) and massPrior(1) earth masses
                if params["mass_prior"][0] == "lin":
                    cube[j] = params["mass_prior"][1] + (params["mass_prior"][2] - params["mass_prior"][1]) * cube[j]  # uniform distributon between massPrior(2) and massPrior(1) earth masses
                if params["mass_prior"][0] != "log" and params["mass_prior"][0] != "lin":
                    print("mass_prior[0] should be either lin or log. Exiting.")
                    exit()

            # delta_ex prior
            for j in range(nPl):
                if params["ex_prior"][0] == "ray":
                    cube[nPl + j] = params["ex_prior"][1] * sqrt(2) * scipy.special.erfinv(2 * cube[nPl + j] - 1)  # Gaussian distribution for ex(j)-ex(j-1)
                if params["ex_prior"][0] == "log":
                    cube[nPl + j] = ( 10 ** params["ex_prior"][1] + (10 ** params["ex_prior"][2] - 10 ** params["ex_prior"][1]) * cube[nPl + j])
                if params["ex_prior"][0] == "lin":
                    cube[nPl + j] = params["ex_prior"][1] + (params["ex_prior"][2] - params["ex_prior"][1]) * cube[nPl + j]
                if params["ex_prior"][0] != "log" and params["ex_prior"][0] != "lin" and params["ex_prior"][0] != "ray":
                      print("ex_prior[0] should be either ray, lin or log. Exiting.")
                      exit()

            # delta_ey prior
            for j in range(nPl):
                if params["ey_prior"][0] == "ray":
                    cube[2 * nPl + j] = params["ey_prior"][1] * sqrt(2) * scipy.special.erfinv(2 * cube[2 * nPl + j] - 1)  # Gaussian distribution for ex(j)-ex(j-1)
                if params["ey_prior"][0] == "log":
                    cube[2 * nPl + j] = ( 10 ** params["ey_prior"][1] + (10 ** params["ey_prior"][2] - 10 ** params["ey_prior"][1]) * cube[2 * nPl + j])
                if params["ey_prior"][0] == "lin":
                    cube[2 * nPl + j] = params["ey_prior"][1] + (params["ey_prior"][2] - params["ey_prior"][1]) * cube[2 * nPl + j]
                if params["ey_prior"][0] != "log" and params["ey_prior"][0] != "lin" and params["ey_prior"][0] != "ray":
                      print("ey_prior[0] should be either ray, lin or log. Exiting.")
                      exit()

        # Defining a likelihood function
        def loglike(cube, nDim, nPar):

            nPl = params["nPl"]

            mass = np.array([cube[j] for j in range(nPl)])
            exd = np.array([cube[nPl + j] for j in range(nPl)])
            eyd = np.array([cube[2 * nPl + j] for j in range(nPl)])

            ModelLogLike = model(mass, exd, eyd, nPl)

            return ModelLogLike

        #### Initiating MultiNest ####
        pymultinest.run(loglike, prior, n_dims = nDim, n_params = nPar, outputfiles_basename = params["basename"], sampling_efficiency = params["sampling_efficiency"], evidence_tolerance = params["evidence_tolerance"], resume = False, verbose = True, multimodal = True)

#### MultiNest data analyzer and plotter ####
def multinest_analyzer(params, analyzer_params, Dyn_Params, Phot_Params, Integration_Params, Paths):

    import pymultinest
    BestFitVal = "maximum"
    fontsize = analyzer_params["fontsize"]

    #### Percentiles
    percentile1 = (68.2689492137086) / 2
    percentile2 = (95.4499736103642) / 2
    percentile3 = (99.7300203936740) / 2
    percentile4 = (99.9936657516334) / 2
    percentile5 = (99.9999426696856) / 2

    sigma1 = 68.2689492137086 / 100.
    sigma2 = 95.4499736103642 / 100.
    sigma3 = 99.7300203936740 / 100.
    sigma4 = 99.9936657516334 / 100.
    sigma5 = 99.9999426696856 / 100.
    sigmas = [0., sigma1, sigma2, sigma3, sigma4, sigma5]

    if params["mode"] == "TTVFaster":

        nPl = params["nPl"]

        df_sigmas = np.array([scipy.stats.chi2.ppf(sigmas[i], 3 * nPl) for i in range(len(sigmas))]) # Chi2 equivalent for normal distribution with 3 * nPl degrees of freedom

        #### Loading MultiNest posterior distributions ####
        multinest_output = pymultinest.Analyzer(outputfiles_basename = params["basename"], n_params = 3 * params["nPl"])

        data = multinest_output.get_data()
        mode_stats = multinest_output.get_mode_stats()

        chi2 = np.array(data[:, 1]) # All chi2
        minchi2_index = np.argmin(chi2) # Index of smallest chi2
        min_chi2 = chi2[minchi2_index] # Smallest chi2 value
        delta_chisqr = np.array(chi2 - min_chi2) # Subtracting min_chi2 from chi2 to receive delta_chi2 posteriors

        idx_sigma5 = [b for b, x in enumerate(delta_chisqr) if x <= df_sigmas[5]]  # Disposing of burn-out (values within 5-sigma range)
        idx_sigma4 = [b for b, x in enumerate(delta_chisqr) if x <= df_sigmas[4]]  # Disposing of burn-out (values within 4-sigma range)
        idx_sigma3 = [b for b, x in enumerate(delta_chisqr) if x <= df_sigmas[3]]  # Disposing of burn-out (values within 3-sigma range)
        idx_sigma2 = [b for b, x in enumerate(delta_chisqr) if x <= df_sigmas[2]]  # Disposing of burn-out (values within 2-sigma range)
        idx_sigma1 = [b for b, x in enumerate(delta_chisqr) if x <= df_sigmas[1]]  # Disposing of burn-out (values within 2-sigma range)

        best_fit_masses = np.zeros(nPl)
        best_fit_ex = np.zeros(nPl)
        best_fit_ey = np.zeros(nPl)

        #### Quoting MultiNest best-fits and errors ####
        for m in range(len(mode_stats["modes"])):
            print("mode {}:".format(m))
            for i in range(nPl):
                print("  mass{0} = {1} +/- {2} [earth_mass]".format(i, mode_stats["modes"][m][BestFitVal][i], mode_stats["modes"][m]["sigma"][i]))
                best_fit_masses[i] = mode_stats["modes"][m][BestFitVal][i]
            for i in range(nPl):
                print("  exd{0} = {1} +/- {2}".format(i, mode_stats["modes"][m][BestFitVal][nPl + i], mode_stats["modes"][m]["sigma"][nPl + i]))
                best_fit_ex[i] = mode_stats["modes"][m][BestFitVal][nPl + i]
            for i in range(nPl):
                print("  eyd{0} = {1} +/- {2}".format(i, mode_stats["modes"][m][BestFitVal][2 * nPl + i], mode_stats["modes"][m]["sigma"][2 * nPl + i]))
                best_fit_ey[i] = mode_stats["modes"][m][BestFitVal][2 * nPl + i]

        data = transpose(data)

        if analyzer_params["plot_posterior"] == True:

            for i in range(nPl):

                masses = data[2 + i]
                ex = data[2 + nPl + i]
                ey = data[2 + 2 * nPl + i]

                plt.figure(4)
                plt.subplot(3,1,1)
                plt.title("Best-fit Likelihood = " +str(round(min(abs(chi2)), 1)) + " [$-log(\mathscr{L})$]", fontsize = fontsize)
                plt.ylabel("$-\Delta log(\mathscr{L})$", fontsize = fontsize)
                plt.plot(masses[idx_sigma5], delta_chisqr[idx_sigma5], 'o', label = '5$\sigma$')
                plt.plot(masses[idx_sigma4], delta_chisqr[idx_sigma4], 'o', label = '4$\sigma$')
                plt.plot(masses[idx_sigma3], delta_chisqr[idx_sigma3], 'o', label = '3$\sigma$')
                plt.plot(masses[idx_sigma2], delta_chisqr[idx_sigma2], 'o', label = '2$\sigma$')
                plt.plot(masses[idx_sigma1], delta_chisqr[idx_sigma1], 'o', label = '1$\sigma$')
                plt.xlabel("Mass [m$_\oplus$]", fontsize = fontsize)
                plt.tick_params(labelsize = fontsize)
                plt.legend()
                plt.subplot(3,1,2)
                plt.plot(ex[idx_sigma5], delta_chisqr[idx_sigma5], 'o', label = '5$\sigma$')
                plt.plot(ex[idx_sigma4], delta_chisqr[idx_sigma4], 'o', label = '4$\sigma$')
                plt.plot(ex[idx_sigma3], delta_chisqr[idx_sigma3], 'o', label = '3$\sigma$')
                plt.plot(ex[idx_sigma2], delta_chisqr[idx_sigma2], 'o', label = '2$\sigma$')
                plt.plot(ex[idx_sigma1], delta_chisqr[idx_sigma1], 'o', label = '1$\sigma$')
                if i == 0:
                    plt.xlabel("e$_x,0$", fontsize = fontsize)
                else:
                    plt.xlabel("$\Delta$e$_x$", fontsize = fontsize)
                plt.ylabel("$-\Delta log(\mathscr{L})$", fontsize = fontsize)
                plt.tick_params(labelsize = fontsize)
                plt.subplot(3,1,3)
                plt.plot(ey[idx_sigma5], delta_chisqr[idx_sigma5], 'o', label = '5$\sigma$')
                plt.plot(ey[idx_sigma4], delta_chisqr[idx_sigma4], 'o', label = '4$\sigma$')
                plt.plot(ey[idx_sigma3], delta_chisqr[idx_sigma3], 'o', label = '3$\sigma$')
                plt.plot(ey[idx_sigma2], delta_chisqr[idx_sigma2], 'o', label = '2$\sigma$')
                plt.plot(ey[idx_sigma1], delta_chisqr[idx_sigma1], 'o', label = '1$\sigma$')
                if i == 0:
                    plt.xlabel("e$_y,0$", fontsize = fontsize)
                else:
                    plt.xlabel("$\Delta$e$_y$", fontsize = fontsize)
                plt.ylabel("$-\Delta log(\mathscr{L})$", fontsize = fontsize)
                plt.tick_params(labelsize = fontsize)
                plt.show()

        #### Calculating errors independent of MultiNest ####
        mass_err = []
        ex_err = []
        ey_err = []

        if analyzer_params["err"] == "chi2":

            for i in range(nPl):
                mass_err.append([best_fit_masses[i] - np.min(data[2 + i][idx_sigma1]), np.max(data[2 + i][idx_sigma1]) - best_fit_masses[i]])
                ex_err.append([best_fit_ex[i] - np.min(data[2 + nPl + i][idx_sigma1]), np.max(data[2 + nPl + i][idx_sigma1]) - best_fit_ex[i]])
                ey_err.append([best_fit_ey[i] - np.min(data[2 + 2 * nPl + i][idx_sigma1]), np.max(data[2 + 2 * nPl + i][idx_sigma1]) - best_fit_ey[i]])
        if analyzer_params["err"] == "percentile":

            for i in range(nPl):

                #### Calculating mass percentile error ####
                mass_med = np.median(data[2 + i][idx_sigma3])
                mass_err_up = np.percentile(data[2 + i][idx_sigma3], 50 + percentile1) - mass_med
                mass_err_down = mass_med - np.percentile(data[2 + i][idx_sigma3], 50 - percentile1)

                #### Calculating delta_ex percentile error ####
                ex_med = np.median(data[2 + nPl + i][idx_sigma3])
                ex_err_up = np.percentile(data[2 + nPl + i][idx_sigma3], 50 + percentile1) - ex_med
                ex_err_down = ex_med - np.percentile(data[2 + nPl + i][idx_sigma3], 50 - percentile1)

                #### Calculating delta_ey percentile error ####
                ey_med = np.median(data[2 + 2 * nPl + i][idx_sigma3])
                ey_err_up = np.percentile(data[2 + 2 * nPl + i][idx_sigma3], 50 + percentile1) - ey_med
                ey_err_down = ey_med - np.percentile(data[2 + 2 * nPl + i][idx_sigma3], 50 - percentile1)

                mass_err.append([mass_err_down, mass_err_up])
                ex_err.append([ex_err_down, ex_err_up])
                ey_err.append([ey_err_down, ey_err_up])

                best_fit_masses[i] = mass_med
                best_fit_ex[i] = ex_med
                best_fit_ey[i] = ey_med
        if analyzer_params["err"] != "chi2" and analyzer_params["err"] != "percentile":
            print("err can only be chi2 or percentile. Exiting.")
            exit()

        print("\n Independent best-fit parameter estimation (using {0} method): \n".format(analyzer_params["err"]))
        for i in range(nPl):
            print("Planet {0}:".format(i))
            print("Mass: {0} +{1}, -{2} [m_earth]".format(best_fit_masses[i], mass_err[i][1], mass_err[i][0]))
            print("delta_ex: {0} +{1}, -{2}".format(best_fit_ex[i], ex_err[i][1], ex_err[i][0]))
            print("delta_ey: {0} +{1}, -{2} \n".format(best_fit_ey[i], ey_err[i][1], ey_err[i][0]))

        #### Generating corner plot ####
        if analyzer_params["plot_corner"] == True:

            import corner

            all_params = []
            labels = []

            for i in range(nPl):
                all_params.append(np.array(data[2 + i][idx_sigma3]))
                all_params.append(data[2 + nPl + i][idx_sigma3])
                all_params.append(data[2 + 2 * nPl + i][idx_sigma3])
                labels.append("m{0}".format(i))
                if i == 0:
                    labels.append("$e_x{0}$".format(i))
                    labels.append("$e_y{0}$".format(i))
                else:
                    labels.append("$\Delta e_x{0}$".format(i))
                    labels.append("$\Delta e_y{0}$".format(i))

            plt.figure(5)
            figure = corner.corner(transpose(all_params), labels = labels, quantiles=[0.16, 0.5, 0.84], show_titles=True, title_kwargs={"fontsize": 16})
            plt.show()

        #### Plotting best-fit light-curve ####
        if analyzer_params["plot_bestfit_LC"] == True:

            #### Turning the delta_ex, delta_ey values into absolute eccentricity components
            ex = np.array([best_fit_ex[0]] + [best_fit_ex[0] + best_fit_ex[i] for i in range(1, nPl)])
            ey = np.array([best_fit_ey[0]] + [best_fit_ey[0] + best_fit_ey[i] for i in range(1, nPl)])

            Dyn_Params["masses"] = best_fit_masses
            Dyn_Params["ecosomega"] = ex
            Dyn_Params["esinomega"] = ey

            #### Generating model ####
            bestFit_model = LightCurve_Gen(Dyn_Params, Phot_Params, Integration_Params, Paths, False)["lightcurve_allPlanets"]

            plt.figure(6)
            plt.title("Best-fit model vs. data", fontsize = fontsize)
            plt.plot(Phot_Params["LC_times"], params["data_LC"], 's', color = 'black', label = 'Data')
            plt.plot(Phot_Params["LC_times"], bestFit_model, color = 'orange', label = 'Best-fit model')
            plt.xlabel("Time [days]", fontsize = fontsize)
            plt.ylabel("Norm. Flux", fontsize = fontsize)
            plt.legend(fontsize = fontsize)
            plt.tick_params(labelsize = fontsize)
            plt.show()