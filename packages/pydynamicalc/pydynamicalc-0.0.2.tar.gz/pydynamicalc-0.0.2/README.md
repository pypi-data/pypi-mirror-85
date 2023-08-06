# PyDynamicaLC
Pythonic photodynamical model generator, using three different configurations (quasi-circular, eccentric and osculating), in addition - an MCMC-coupled version is also provided, which allows optimization of planetary masses and eccentricities as presented in [Yoffe et al. (2020)](link). NOTE: please refer to our paper and the README provided here to fully fathom the approximations utilized in each of the configurations in this code.

All functions in PyDyamicaLC must be imported, such that when integrated in a script, import as follows (see example script):

from PyDynamicaLC import *

List of ALL external Python libraries used: Pylab, Scipy, PyAstronomy, PyMultiNest, ttvfaster, corner, os

The code was tested on a Linux and OSx platform.

The code relies on several existing open-source routines, the links to and installation guides of are listed below.

The package was developed within the research group of Prof. Oded Aharonson, Weizmann Institute of Science, Israel.

PyAstronomy
=======

This routine is used to generate a Mandel-Agol light-curve

Information regarding installation can be found here: https://github.com/sczesla/PyAstronomy


TTVFast (C) - NOTE: the required modified version may only be downloaded here
=======

This routine is one out of two possibilities to simulate planetary dynamics (the other being TTVFaster). TTVFast is a simplectic n-body integrator, whereas TTVFaster is a semi-analytic model accurate to first order in eccentricity which approximates TTVs using a series expansion.

We modified TTVFast to output the instantaneous osculating Keplerian parameters at each time of mid-transit, with which each individual transit shape and timing is determined in the "osculating" mode.

The C version of the code is in the directory c_version, the Fortran version is in fortran_version. Both versions have specific README files.

All associated information regarding TTVFast (C) can be found here: https://github.com/kdeck/TTVFast/tree/master/c_version

TTVFaster
=======

This routine is one out of two possibilities to simulate planetary dynamics (the other being TTVFast). TTVFast is a simplectic n-body integrator, whereas TTVFaster is a semi-analytic model accurate to first order in eccentricity which approximates TTVs using a series expansion.

Information regarding installation can be found here: https://github.com/ericagol/TTVFaster

PyMultiNest
=======

A multi-modal Markov Chain Monte Carlo algorithm with implementation in Python used as our fitter of choice.

Information regarding installation can be found here: https://johannesbuchner.github.io/PyMultiNest/

INPUT
===

Each of the following is a dictionary which should contain the exact entries listed here.

## Integration_Params:
    # t_min = time of the start of integration [days]
    # t_max = time of the endof integration [days]
    # dt = time step during the integration [days]

## Paths:
    # dyn_path: Path to TTVFast folder (should end with "c_version/")
    # dyn_path_OS: Same path as dyn_path, except that it should be compatible with OS
    # dyn_file_name: This file is internally used by TTVFast to receive the initial condition and integration parameters. This string is the header of file - make sure to change it if several simulations are run simultaneously
    # Coords_output_fileName: name of the desired cartesian coordinates file from TTVFast.

## Phot_Params: PHOTOMETRIC PARAMETERS
    # LC_times: list of times for which the lightcurve will be sampled [days]
    # LDcoeff1: linear limb-darkening coefficient
    # LDcoeff2: quadratic limb-darkening coefficient
    # r = numpy array of relative planet radii [r/R_star]
    # transit_width: a phase-window used to refine the time of mid-transit. if A is the max-TTV-amplitude, then transit_width should be more than the [transit duration + A] and significantly less than [0.5 - A]. Default: 0.05.
    # ReBin_N: PyAstronomy parameter used to simulate the finite exposure time (following Kipping 2010). N is the number of subsamples, dispersed over a time span of dt.
    # ReBin_dt: PyAstronomy parameter used to simulate the finite exposure time (following Kipping 2010). dt is the cadence time.

## Dyn_Params: DYNAMICAL PARAMETERS
    # LC_mode: string specifying which mode of lightcurve generation to use. Can be "osc", "ecc" or "circ" (osculating, eccentric and quasi-circular, respectively)
    # m_star: stellar mass [m_sun]
    # r_star: stellar radius [r_sun]
    # masses: vector of planetary masses [m_earth]

    ### OSCULATING LIGHTCURVE - Keplerian parameters are the INITIAL CONDITIONS ###
    # dyn_coords: for LC_mode = osc, the initial conditions input can be input as either the Keplerian parameters or a Cartesian state vector. The six-element input has to be specified as follows:

    # if dyn_coords == "keplerian":
        # p: vector of planetary orbital periods at t_min [days]
        # incs: vector of planetary inclinations at t_min [deg]
        # Omegas: vector of planetary inclinations at t_min [deg]
        # ecosomega: vector of planetary ecos(omega)s at t_min
        # esinomega: vector of planetary esin(omega)s at t_min
        # tmids: vector of first times of mid-transit for each planet [days]

    if dyn_coords == "cartesian":
        position_vec: vector of x, y, z position of each planet at t_min, in AU. Mind that the z coordinate should have its sign opposite from the convention (i.e. z -> -z)
        velocities_vec: vector of x_dot, y_dot, z_dot velocities of each planet at t_min, in AU/day. Same coordiantes system as [x, y, z].

    ### ECCENTRIC/QUASI-CIRCULAR LIGHTCURVE - Keplerian parameters are AVERAGE values ###
    # p: vector of average planetary orbital periods [days]
    # incs: vector of average planetary inclinations [deg]
    # Omegas: vector of average planetary longitudes of ascending node [deg]
    # ecosomega: vector of average planetary ecos(omega)s [deg]
    # esinomega: vector of average planetary esin(omega)s [deg]
    # tmids: vector of initial times of transit (according to the mean ephemeris) [days]

## To initiate light-curve generator (LightCurve_Gen):LightCurve_Gen(Dyn_Params, Phot_Params, Integration_Params, Paths, verbose) (see example script)

RUNNING MULTINEST
===

The following two dictionaries are required to run the MultiNest fitter example. The fitter uses TTVFaster-based dynamical modelling to optimize the planetary masses, delta_ex and delta_ey (ex and ey for the inner planets) of the input system. Since TTVFaster is currently the only option for the optimization routine, LC_mode should either be "circ" or "ecc".

 ## MultiNest_params: Optimization parameters for MultiNest
    # mode: Optimization mode. At this moment, this can only be "TTVFaster" (string)
    # data_LC: normalized flux of the multi-planet data light-curve. Should be the length of LC_times (np.array)
    # data_LC_err: errors of the normalized flux light-curve. Should be the length of data_LC/LC_times (np.array)
    # nPl: number of planets (integer)
    # mass_prior: list specifying mass prior parameters. Supposed to contain 3 components: "lin" or "log" strings specifying linear or logarithmic prior, and lower and upper limit numbers. In the case of "lin", the limit numbers are the absolute mass limits of the prior in [m_earth]. In the case of "log" the limit numbers are *powers* (of base ten) of the prior (the whole number in units of m_earth). For e.g.: ["lin" 2 20] will search in the range of 2 to 20  Earth masses, while ["log" -1 3] will search in the range of 0.1 to 1000 Earth masses.
    # ex_prior: list specifying ecosomega prior. Similar to mass_prior with units of eccentricity, but in addition - a Rayleigh distribution of the prior can be chosen with a string "ray", then there is only one additional required number in the list - the scale-width of the distribution.
    # ey_prior: similar to ex_prior.
    # verbose: Boolean.
    # basename: a string containing the header of all MultiNest files to be generated
    # sampling_efficiency: MultiNest parameter (see https://johannesbuchner.github.io/PyMultiNest/). Recommended value: 0.5.
    # evidence_tolerance: MultiNest parameter (see link above). Recommended value: 0.01.

## Analyzer_params: Posterior distribution analysis, error-estimation and plotting of MultiNest output
    # err: can be either "percentile" or "chi2" (string). This performs a MultiNest-independent error estimation in the following manner:
        percentile: using the loglike output, only points with relative likelihood $<10^{-3}$ times that of the best-fit are considered ("burn-in"). The the ±1sigma uncertainties are then the 16th and 84th percentiles of the remaing points.
        chi2: the ±1sigma uncertainties are calculatesd using the absolute difference of the best-fit value and the minimal and maximal values in the 1sigma range of delta_chi2.
        # fontsize: fontsize of the plots (float/int)
        # plot_posterior: Boolean. If true - plots the MultiNest posterior distribution for all parameters. 1-5 sigma ranges are color-coded.
        # plot_bestfit_LC: Boolean. If true - plots generates a light-curve with the best-fit values and plots it against the data.
        # plot_corner: uses corner.py (https://corner.readthedocs.io/en/latest/) to generate corner plots for all parameters within the delta_chi2 < 3sigma range. NOTE: this option requires corner.py to be installed!

 ## To initiate MultiNest fitter: run_multinest(MultiNest_params, Dyn_Params, Phot_Params, Integration_Params, Paths) (see example script)
 ## To initiate MultiNest analyzer: multinest_analyzer(params, analyzer_params, Dyn_Params, Phot_Params, Integration_Params, Paths) (see example script)

OUTPUT
===

## LightCurve_Gen:
    This function returns a dictionary containing the following entries:
        # times: list of lists of times of mid-transit for all planets [days]
        # ttvs: list of lists of TTVs for all planets [days]
        # lin_eph: list of lists of times of mean ephemeris mid-transit times for all planets [days]
        # lightcurve_singlePlanets: list of light-curves for individual planets separately [norm. flux]
        # lightcurve_allPlanets: single multi-planet light-curve [norm. flux]

## run_multinest:
    Once this function is initiated - MultiNest optimization commences.

## multinest_analyzer:
    This function analyzes multinest output and plots relevant plots, as described above.

 CLARIFICATION REGARDING t_mid FOR OSCULATING AND ECCENTRIC/QUASI-CIRCULAR CASES:

 Osculating: in this case, t_mid is simply the time of the first time of mid-transit with respect to t_min. The phase of the planet is then calculated by "rewinding" a Keplerian arc from that point to t_min (note: this is an approximation that may not be valid in very eccentric systems).

 Eccentric/quasi-Circular: In this case, the value t_min represents the LINEAR APPROXIMATION of the first time of mid-transit. That is, the time of mid-transit of the given epoch in a linear ephemeris regime (we extracted this value by fitting a line to the observed times of transit. The value t_mind would then be the value of the fitted line at the given epoch).

Citations
=======

If you use this code, please cite [Yoffe et al. (2020)](link).

For TTVFast, please cite [Deck &amp; Agol (2014)](https://iopscience.iop.org/article/10.1088/0004-637X/787/2/132/pdf).

For TTVFaster, please cite [Agol &amp; Deck (2015)](http://arxiv.org/abs/1509.01623).

For MultiNest and PyMultiNest, please cite [Feroz et al. (2008)](https://arxiv.org/abs/0809.3437), [Buchner et al. (2014)](https://www.aanda.org/articles/aa/abs/2014/04/aa22971-13/aa22971-13.html), respectively.

Please check back for updates to ensure that you are using the latest version.

-Gideon Yoffe, Aviv Ofir and Oded Aharonson
