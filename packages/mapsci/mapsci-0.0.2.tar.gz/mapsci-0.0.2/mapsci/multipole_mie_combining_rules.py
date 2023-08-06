"""

MAPSCI: Multipole Approach of Predicting and Scaling Cross Interactions

Handles the primary functions
"""

import numpy as np
import scipy.optimize as spo
import logging

logger = logging.getLogger(__name__)


def calc_distance_array(bead_dict, tol=0.01, max_factor=2, lower_bound="rmin"):
    r"""
    Calculation of array for nondimensionalized distance array.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    bead_dict : dict
        Dictionary of multipole parameters.
        
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    tol : float, Optional, default=0.01
        Ratio of absolute value of repulsive term over attractive term of the Mie potential to define minimum bound
    max_factor : int, Optional, default=2
        Factor to multiply minimum bound by to define maximum bound.
    lower_bound : str, Optional, default='rmin'
        Lower bound of distance array. Can be one of:

        - rmin: the position of the potential well
        - sigma: the size parameter
        - tolerance: Uses 'tol' keyword to define the ratio between the attractive and repulsive terms of the Mie potential, note that if tol = 0.01 the lower bound will be ~2.5*sigma.
    
    Returns
    -------
    r : numpy.ndarray
        Array (or float) in [Å] or nondimensionalized, distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    """

    if lower_bound == "rmin":
        rm = mie_potential_minimum(bead_dict)
    elif lower_bound == "sigma":
        rm = bead_dict["sigma"]
    elif lower_bound == "tolerance":
        rm = bead_dict["sigma"] * (1 / tol)**(1 / (bead_dict["lambdar"] - bead_dict["lambdaa"]))
    else:
        raise ValueError("Method, {}, is not supported to calculating lower_bound of fitting/integration".format(lower_bound))

    r_array = np.linspace(rm, max_factor * rm, num=10000)

    return r_array

def mie_potential_minimum(bead_dict):
    r"""
    Calculate Mie potential minimum of potential well.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    bead_dict : dict
        Dictionary of multipole parameters.
        
        - sigma (float) Size parameter in [Å] or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    Returns
    -------
    rmin : float
        Position of minimum of potential well
    """

    return bead_dict["sigma"] * (bead_dict["lambdar"] / bead_dict["lambdaa"])**(1 / (bead_dict["lambdar"] - bead_dict["lambdaa"]))


def mie_combining_rules(bead1, bead2):
    r"""
    Calculate basic mixed parameters, where the energy parameter is calculated with the geometric mean

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    Returns
    -------
    beadAB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
    """

    beadAB = {}
    beadAB["sigma"] = (bead1["sigma"] + bead2["sigma"]) / 2
    beadAB["lambdar"] = 3 + np.sqrt((bead1["lambdar"] - 3) * (bead2["lambdar"] - 3))
    beadAB["lambdaa"] = 3 + np.sqrt((bead1["lambdaa"] - 3) * (bead2["lambdaa"] - 3))
    beadAB["epsilon"] = np.sqrt(bead1["epsilon"] * bead2["epsilon"])

    return beadAB


def calc_mie_attractive_potential(r, bead_dict, shape_factor_scale=False):
    r"""
    Calculation of attractive Mie potential.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) in either [Å] or nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`, whatever is consistent with 'bead_dict'
    bead_dict : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    
    Returns
    -------
    potential : numpy.ndarray
        Array of nondimensionalized potential between beads from Mie potential. Array is equal in length to "r". :math:`\phi'=\phi/(3k_{B}T)`
    """

    if shape_factor_scale:
        if "Sk" in bead_dict:
            bead_dict["epsilon"] = bead_dict["epsilon"] * bead_dict["Sk"]**2
        else:
            raise ValueError("Shape factor was not provided in bead dictionary")

    potential = -prefactor(bead_dict["lambdar"], bead_dict["lambdaa"]) * bead_dict["epsilon"] * (bead_dict["sigma"] /
                                                                                         r)**bead_dict["lambdaa"]

    return potential

def calc_mie_repulsive_potential(r, bead_dict, shape_factor_scale=False):
    r"""
    Calculation of repulsive Mie potential.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) in either [Å] or nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`, whatever is consistent with 'bead_dict'
    bead_dict : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    
    Returns
    -------
    potential : numpy.ndarray
        Array of nondimensionalized potential between beads from Mie potential. Array is equal in length to "r". :math:`\phi'=\phi/(3k_{B}T)`
    """

    if shape_factor_scale:
        if "Sk" in bead_dict:
            bead_dict["epsilon"] = bead_dict["epsilon"] * bead_dict["Sk"]**2
        else:
            raise ValueError("Shape factor was not provided in bead dictionary")

    potential = prefactor(bead_dict["lambdar"], bead_dict["lambdaa"]) * bead_dict["epsilon"] * (bead_dict["sigma"] /
                                                                                         r)**bead_dict["lambdar"]

    return potential


def prefactor(lamr, lama):
    """ Calculation prefactor for Mie potential: :math:`C_{Mie}=\lambda_r/(\lambda_r-\lambda_a) (\lambda_r/\lambda_a)^{\lambda_a/(\lambda_r-\lambda_a)}`
    """

    return lamr / (lamr - lama) * (lamr / lama)**(lama / (lamr - lama))


def calc_lambdaij_from_epsilonij(epsij, bead1, bead2):
    r"""
    Calculates cross-interaction exponents from cross interaction energy parameter

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    epsilonij : float
        Fit energy parameter in [K] or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    Returns
    -------
    lambdar_new : float
        Repulsive exponent
    lambdaa_new : float
        Attractive exponent 
    """

    sigmaij = np.mean([bead1["sigma"], bead2["sigma"]])
    tmp = epsij * sigmaij**3 / np.sqrt(bead1["sigma"]**3 * bead2["sigma"]**3) / np.sqrt(
        bead1["epsilon"] * bead2["epsilon"])
    lamr_ij = 3 + tmp * np.sqrt((bead1["lambdar"] - 3) * (bead2["lambdar"] - 3))
    lama_ij = 3 + tmp * np.sqrt((bead1["lambdaa"] - 3) * (bead2["lambdaa"] - 3))

    return lamr_ij, lama_ij

def calc_epsilonij_from_lambda_aij(lambda_a, bead1, bead2):
    r"""
    Calculate cross-interaction energy parameter from self-interaction parameters and cross-interaction attractive exponent using from scaling with vdW attraction parameter

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    lambda_aij : float
        Mixed attractive exponent from multipole combining rules
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    Returns
    -------
    epsilon_ij : float
        Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
    """

    tmp_sigma = np.sqrt(bead1["sigma"]**3 * bead2["sigma"]**3) / np.mean([bead1["sigma"], bead2["sigma"]])**3
    tmp_lambda = (lambda_a - 3) / np.sqrt((bead1["lambdaa"] - 3) * (bead2["lambdaa"] - 3))
    epsilon_ij = np.sqrt(bead1["epsilon"] * bead2["epsilon"]) * tmp_sigma * tmp_lambda

    return epsilon_ij

def calc_lambdarij_from_lambda_aij(lambda_a, alpha_mie):
    r"""
    Calculate cross-interaction repulsive exponent from cross interaction attractive exponent and Mie 'vdW like' interaction parameter.

    Parameters
    ----------
    lambda_aij : float
        Mixed attractive exponent from multipole combining rules
    alpha_mie : float
        This nondimensionalized attractive parameter for the Mie potential is related not only to the Mie exponents but also to the triple and critical temperatures of a substance.  

    Returns
    -------
    lambdar_new : float
        Repulsive exponent
    """

    lambda_r = spo.brentq(lambda x: alpha_mie - prefactor(x, lambda_a) * (1 / (lambda_a - 3) - 1 / (x - 3)),
                          lambda_a * 1.01,
                          1e+4,
                          xtol=1e-12)

    return lambda_r

def calc_self_multipole_potential(r, polarizability, bead_dict, temperature=None, nondimensional=False):
    r"""
    Calculation of self-interaction potential using extended multipole expression, either with or without dimensions

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) of nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    polarizability : float
        Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
    bead_dict : dict
        Dictionary of multipole parameters. Those parameters may be:
        
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Nondimensionalize polarizability of bead in [:math:`Å^3`]. :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`

    Returns
    -------
    potential : numpy.ndarray
        Multipole potential between beads based on multipole moments that is in [kcal/mol], or nondimensionalized as :math:`\phi'=\phi/(3k_{B}T)` Array is equal in length to "r".

    """

    bead_dict["polarizability"] = polarizability

    if not nondimensional:
        if temperature == None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead_dict_new = dict_dimensions(bead_dict.copy(), temperature, dimensions=False)
        r = float_dimensions(r,"sigma",temperature,dimensions=False)
    else:
        bead_dict_new = bead_dict.copy()

    t11 = -bead_dict_new["charge"]**2 * bead_dict_new["dipole"]**2
    t12 = -bead_dict_new["charge"]**2

    t21 = -3 * bead_dict_new["ionization_energy"] / 4
    t22 = -2 * bead_dict_new["dipole"]**2
    t23 = -bead_dict_new["dipole"]**4 - 3 * bead_dict_new["quadrupole"]**2 * bead_dict_new["charge"]**2 / 5

    t31 = -3 * bead_dict_new["dipole"]**2 * bead_dict_new["quadrupole"]**2
    t32 = -3 * bead_dict_new["quadrupole"]**2

    t41 = -21 / 5 * bead_dict_new["quadrupole"]**4

    potential = (t11 + bead_dict_new["polarizability"]*t12)/r**4 \
              + (t21*bead_dict_new["polarizability"]**2 + t22*bead_dict_new["polarizability"] + t23)/r**6 \
              + (t31 + bead_dict_new["polarizability"]*t32)/r**8 \
              + t41/r**10

    if not nondimensional:
        potential = float_dimensions(potential,"ionization_energy",temperature,dimensions=True)

    return potential

def calc_polarizability(bead_library, temperature=None, distance_opts={}, calculation_method="fit", polarizability_opts={}, nondimensional=False, shape_factor_scale=False):
    r"""
    Calculation of polarizability for beads in the provided library that do not have one calculated. The multipole moments and Mie parameters must be provided for this purpose.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    bead_library : dict
        Dictionary of beads and their dictionaries of multipole parameters. Those parameters may be:
        
        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`

    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    distance_opts : dict, Optional, default={}
        Dictionary of keyword arguments for :func:`~mapsci.multipole_mie_combining_rules.calc_distance_array`
    calculation_method : str, Optional, default="fit"
        Method of calculating the polarizability, either 'fit' or 'analytical'
    polarizability_opts : dict, Optional, default={}
        Dictionary of keyword arguments for :func:`~mapsci.multipole_mie_combining_rules.fit_polarizability` or :func:`~mapsci.multipole_mie_combining_rules.solve_polarizability_integral`
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    
    Returns
    -------
    bead_library : dict
        Dictionary of beads and their dictionaries of multipole parameters. The following parameter is added to the original dictionary:

        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized as :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume


    """

    if not nondimensional:
        if temperature == None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead_library_new = dict_dimensions(bead_library.copy(), temperature, dimensions=False)
    else:
        bead_library_new = bead_library.copy()

    tmp = [False if type(value)==dict else True for _,value in bead_library_new.items()]
    if np.all(tmp):
        bead_library_new = {"tmp": bead_library_new}
        flag = True
    elif np.any(tmp):
        raise ValueError("Dictionary should be either a single beads parameters, or a dictionary of dictionaries containing the parameters of several beads.")
    else:
        flag = False

    for i, bead in enumerate(bead_library_new.keys()):
        if "polarizability" in bead_library_new[bead]:
            logger.info("Using given polarizability value for bead, {}".format(bead))
        r = calc_distance_array(bead_library_new[bead], **distance_opts)

        if calculation_method == "fit":
            pol_tmp, var = fit_polarizability(r, bead_library_new[bead], **polarizability_opts, nondimensional=True)
        elif calculation_method == "analytical":
            pol_tmp = solve_polarizability_integral(r[0], bead_library_new[bead], **polarizability_opts, nondimensional=True)
        else:
            raise ValueError("Given, {}, is not a valid calculation method, choose 'fit' or 'analytical'".format(calculation_method))

        if np.isnan(pol_tmp):
            raise ValueError("Error: Bead {} cannot fit suitable polarizability. Attractive exponent is most likely not suitable given the bead partial charges.")
        bead_library_new[bead]["polarizability"] = pol_tmp

    if not nondimensional:
        bead_library_new = dict_dimensions(bead_library_new, temperature, dimensions=True)

    if flag:
        bead_library_new = bead_library_new["tmp"]

    return bead_library_new


def fit_polarizability(r, bead_dict, temperature=None, nondimensional=False, tol=0.05, shape_factor_scale=False, plot_fit=False):
    r"""
    Calculation of polarizability by fitting the sum of multipole potentials to attractive term of Mie potential.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) of distance between two beads. Reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    bead_dict : dict
        Dictionary of multipole parameters.
        
        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`

    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    tol : float, Optional, default=0.05
        Ratio of variance of polarizability over polarizability, taken from curve-fit
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    plot_fit : bool, Optional, default=False
        Plot Mie potential and Multipole potential for comparison.
    
    Returns
    -------
    Polarizability : float
        Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
    standard_dev : float
        One standard deviation error for polarizability
    """

    if not nondimensional:
        if temperature == None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead_dict_new = dict_dimensions(bead_dict.copy(), temperature, dimensions=False)
    else:
        bead_dict_new = bead_dict.copy()

    w_mie = calc_mie_attractive_potential(r, bead_dict_new, shape_factor_scale=shape_factor_scale)

    p0 = [1.e-6]
    pol_tmp, var_matrix = spo.curve_fit(
        lambda x, a: calc_self_multipole_potential(x,
                                                   a,
                                                   bead_dict_new,
                                                   nondimensional=True,
                                                   ),
        r,
        w_mie,
        p0=p0,
        bounds=(0.0, np.inf))

    if np.diag(var_matrix) / pol_tmp > tol:
        _ = test_polarizability(pol_tmp, bead_dict_new, r, plot_fit=plot_fit, shape_factor_scale=shape_factor_scale)

    polarizability = pol_tmp[0]
    pol_variance = var_matrix[0][0]

    if not nondimensional:
        polarizability = float_dimensions(polarizability,"polarizability",temperature,dimensions=True)
        pol_variance = float_dimensions(pol_variance,"polarizability",temperature,dimensions=True)

    return polarizability, pol_variance

def test_polarizability(polarizability, bead_dict, r, plot_fit=False, shape_factor_scale=False):
    r"""
    If polarizability doesn't provide a good fit between multipole potential and Mie potential, use estimated polarizability to suggest a different attractive exponent and energy parameter.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    polarizability : float
        Nondimensionalized polarizability of bead. :math:`\alpha'=\alpha (4 \pi \varepsilon_{0})^{2} 3k_{B}T  e^{-6}`
    bead_dict : dict
        Dictionary of multipole parameters.
        
        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Nondimensionalized charge of bead. :math:`q'=q/e`
        - dipole (float) Nondimensionalized dipole of bead. :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Nondimensionalized quadrupole of bead. :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Nondimensionalized ionization_energy of bead. :math:`I'=I/(3k_{B}T)`

    r : numpy.ndarray
        Array (or float) of nondimensionalized distance between two beads. Nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    plot_fit : bool, Optional, default=False
        Plot Mie potential and Multipole potential for comparison.
    
    Returns
    -------
    epsilon_fit : float
        Energy parameter with curve fit against multipole potential using fit polarizability
    """

    bead_dict_new = bead_dict.copy()

    bead_dict_new["polarizability"] = polarizability
    output = fit_multipole_cross_interaction_parameter(bead_dict_new, 
                                                       bead_dict_new, 
                                                       distance_array=r, 
                                                       nondimensional=True, 
                                                       shape_factor_scale=shape_factor_scale)

    logger.warning(
        "Refitting attractive exponent with estimated polarizability of {} yields: lamba_a {}, epsilon {}".format(
            bead_dict_new["polarizability"], output["lambdaa"], output["epsilon"]))

    if plot_fit:
        from mapsci.quick_plots import plot_potential, plot_multipole_potential

        w_mie = calc_mie_attractive_potential(r, bead_dict_new, shape_factor_scale=shape_factor_scale)
        plot_opts = {"label":"Mie", "color": "k", "linestyle": "--"}
        plot_potential(r, w_mie, plot_opts=plot_opts, show=False)

        bead_dict_plot = bead_dict_new.copy()
        bead_dict_plot.update({"epsilon": output["epsilon"], "lambdaa": output["lambdaa"]})
        w_mie_fit = calc_mie_attractive_potential(r, bead_dict_plot, shape_factor_scale=shape_factor_scale)
        plot_opts = {"label":"Mie fit", "color": "r", "linestyle": "--"}
        plot_potential(r, w_mie_fit, plot_opts=plot_opts, show=False)

        multipole_terms = calc_cross_multipole_terms(bead_dict_new, bead_dict_new, nondimensional=True)
        tmp = ["charge-dipole", "charge-induced_dipole", "induced_dipole-induced_dipole", "dipole-dipole", "dipole-induced_dipole", "charge-quadrupole", "dipole-quadrupole", "induced_dipole-quadrupole", "quadrupole-quadrupole"]
        logger.debug(("{}: {{{}}}\n"*len(tmp)).format(*[val for val in tmp for _ in range(2)]).format(**dict(zip(tmp,A)))) 

        potential, potential_terms = calc_cross_multipole_potential(r, multipole_terms, total_only=False, nondimensional=True)
        plot_multipole_potential(r, potential, potential_terms=potential_terms)

    return output["epsilon"]

def solve_polarizability_integral(sigma0, bead_dict0, shape_factor_scale=False, temperature=None, nondimensional=False):
    r"""
    Calculation of polarizability from multipole moments using explicit integral method.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    sigma0 : float
        This lower bound of the integral dictates where we expect to start matching the multipole attractive term with that of Mie potential. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    bead_dict : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    
    Returns
    -------
    polarizability : float
        Polarizability calculated from Mie and multipole potentials, integrated from sigma0 to infinity. Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
    """

    if not nondimensional:
        if temperature == None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead_dict = dict_dimensions(bead_dict0.copy(), temperature, dimensions=False)
        sigma0 = float_dimensions(sigma0,"sigma",temperature,dimensions=False)
    else:
        bead_dict = bead_dict0.copy()

    Cmie_int = mie_integral(bead_dict, sigma0=sigma0, shape_factor_scale=shape_factor_scale)
    tmp1 = _obj_polarizability_from_integral(np.finfo("float").eps, bead_dict, Cmie_int, sigma0)
    tmp2 = _obj_polarizability_from_integral(1, bead_dict, Cmie_int, sigma0)
    if tmp1 * tmp2 < 0:
        polarizability = spo.brentq(_obj_polarizability_from_integral,
                                    np.finfo("float").eps,
                                    1,
                                    args=(bead_dict, Cmie_int, sigma0),
                                    xtol=1e-12)
    else:
        polarizability = np.nan

    if not nondimensional and not np.isnan(polarizability):
        polarizability = float_dimensions(polarizability,"polarizability",temperature,dimensions=True)

    return polarizability

def calc_cross_multipole_terms(bead1, bead2, temperature=None, nondimensional=False):
    r"""
    Calculation of terms for nondimensionalized cross-interaction potential from multipole moments.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    bead1 : dict
        Dictionary of multipole parameters for bead_A.

        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    bead2 : dict
        Dictionary of multipole parameters for bead_B.

        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`

    Returns
    -------
    multipole_terms : numpy.ndarray
        This list of nine terms terms corresponds to the coefficients the various multipole interactions: charge-dipole, charge-induced_dipole, induced_dipole-induced_dipole, dipole-dipole, dipole-induced_dipole, charge-quadrupole, dipole-quadrupole, induced_dipole-quadrupole, quadrupole-quadrupole
        Note: This are ALWAYS nondimensionalized
    """

    if not nondimensional:
        if temperature == None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        beadA = dict_dimensions(bead1.copy(), temperature, dimensions=False)
        beadB = dict_dimensions(bead2.copy(), temperature, dimensions=False)
    else:
        beadA = bead1.copy()
        beadB = bead2.copy()

    t11 = (beadA['charge']**2. * beadB['dipole']**2 + beadB['charge']**2. * beadA['dipole']**2.) / 2.0
    t12 = (beadA['charge']**2. * beadB['polarizability'] + beadB['charge']**2. * beadA['polarizability']) / 2.0

    I = beadA['ionization_energy'] * beadB['ionization_energy'] / (beadA['ionization_energy'] +
                                                                   beadB['ionization_energy'])

    t21 = 3. * I * beadA['polarizability'] * beadB['polarizability'] / 2.
    t22 = beadA['dipole']**2. * beadB['dipole']**2.
    t23 = beadA['polarizability'] * beadB['dipole']**2. + beadB['polarizability'] * beadA['dipole']**2.
    t24 = 3. * (beadA['quadrupole']**2. * beadB['charge']**2. + beadB['quadrupole']**2. * beadA['charge']**2.) / 10.

    t31 = 3. / 2. * (beadA['dipole']**2. * beadB['quadrupole']**2. + beadB['dipole']**2. * beadA['quadrupole']**2.)
    t32 = 3. / 2. * (beadA['quadrupole']**2. * beadB['polarizability'] +
                     beadB['quadrupole']**2. * beadA['polarizability'])

    t41 = 21. / 5. * beadA['quadrupole']**2. * beadB['quadrupole']**2.

    multipole_terms = np.array([t11, t12, t21, t22, t23, t24, t31, t32, t41], dtype=object)

    return multipole_terms


def condense_multipole_terms(multipole_terms):
    r"""
    The various multipole interactions take place at various orders of distances, ranging from r^(-4) to r^(-10) by orders of 2. This function will take the output of ``calc_cross_multipole_terms`` and combine the appropriate terms to produce 4 coefficients, one for each order of r.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
        
    Parameters
    ----------
    multipole_terms : numpy.ndarray
        This list of nine terms terms corresponds to the coefficients the various multipole interactions: charge-dipole, charge-induced_dipole, induced_dipole-induced_dipole, dipole-dipole, dipole-induced_dipole, charge-quadrupole, dipole-quadrupole, induced_dipole-quadrupole, quadrupole-quadrupole

    Returns
    -------
    new_multipole_terms : numpy.ndarray
        This list of terms corresponds to the coefficients for r to the order of -4, -6, -8, and -10, respectively.
    """

    new_multipole_terms = np.zeros(4)

    new_multipole_terms[0] = np.sum(multipole_terms[:1])
    new_multipole_terms[1] = np.sum(multipole_terms[2:6])
    new_multipole_terms[2] = np.sum(multipole_terms[6:8])
    new_multipole_terms[3] = np.sum(multipole_terms[8])

    return new_multipole_terms


def calc_cross_multipole_potential(r, multipole_terms, nondimensional=False, temperature=None, total_only=True):
    r"""
    Calculation of nondimensionalized cross-interaction potential from multipole moments.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) of nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    multipole_terms : numpy.ndarray
        This can be either a list of terms corresponds to the coefficients for r to the order of -4, -6, -8, and -10, or a list of nine terms terms corresponding to the coefficients the various multipole interactions.
    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    total_only : bool, Optional, default=True
        If true, only the overall potential is returned. This is useful for parameter fitting. If False, the potential for each term is returned in a numpy array.
    
    Returns
    -------
    potential : numpy.ndarray
        Array of nondimensionalized potential between beads based on multipole moments. Array is equal in length to "r". :math:`\phi'=\phi/(3k_{B}T)` or in kcal/mol
    potential_terms : numpy.ndarray, Optional
        2D array of terms involved in multipole moment. Could be 4 terms relating to orders of r from -4 to -10 by steps of 2, or could be the individual contributions. Either dimensionalized or in kcal/mol
        Only provided if ``total_only`` is False
    """

    if np.size(multipole_terms) == 4:
        potential_terms = np.array([
            -multipole_terms[0] / r**4., -multipole_terms[1] / r**6., -multipole_terms[2] / r**8.,
            -multipole_terms[3] / r**10.
        ])
    elif np.size(multipole_terms) == 9:
        potential_terms = np.array([
            -multipole_terms[0] / r**4., -multipole_terms[1] / r**4., -multipole_terms[2] / r**6.,
            -multipole_terms[3] / r**6., -multipole_terms[4] / r**6., -multipole_terms[5] / r**6.,
            -multipole_terms[6] / r**8., -multipole_terms[7] / r**8., -multipole_terms[8] / r**10.
        ])
    else:
        raise ValueError(
            "Multipole terms input should be either of length 4 or length 9 for the supported interaction types.")

    potential = np.sum(potential_terms, axis=0)

    if not nondimensional:
        potential = float_dimensions(potential, "ionization_energy", temperature)
        potential_terms = float_dimensions(potential_terms, "ionization_energy", temperature)

    if total_only:
        return potential
    else:
        return potential, potential_terms

def _obj_polarizability_from_integral(polarizability, bead_dict, Cintegral, sigma0):
    r"""
    Objective function used to determine the polarizability from multipole and Mie integrals from some minimum to infinity
    
    Parameters
    ----------
    polarizability : float
        Guess in nondimensionalized polarizability with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
    bead_dict : dict
        Dictionary of multipole parameters for bead_A.

        - charge (float) Charge nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy nondimensionalized as :math:`I'=I/(3k_{B}T)`

    Cintegral : float
        The Mie integral is set equal to the sum of the multipole potential contributions to determine the polarizability.
    sigma0 : float
        Lower bound of the integral, reported in nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`

    Returns
    -------
    obj_value : float
        Difference between multipole term and Mie potential term integral
    """

    dict_tmp = bead_dict.copy()
    dict_tmp["polarizability"] = polarizability

    Cmultipole, _ = multipole_integral(dict_tmp, dict_tmp, sigma0=sigma0, nondimensional=True)

    return Cmultipole - Cintegral


def partial_polarizability(bead_dict0, temperature=None, sigma0=None, lower_bound="rmin", nondimensional=False):
    r"""
    Calculate partial derivative with respect to multipole moments. This is useful in estimating the error.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    bead_dict : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    temperature : float, Optional, default=298
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    sigma0 : float, Optional, default=None
        This lower bound of the integral dictates where the lower bound of the definite integral is. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    lower_bound : str, Optional, default='rmin'
        Lower bound of distance array. Used only when sigma0 is None. Can be one of:

        - rmin: the position of the potential well
        - sigma: the size parameter

    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    
    Returns
    -------
    partial_dict : dict
        Partial derivative with respect to multipole moments
    """

    if not nondimensional:
        if temperature is None:
            temperature = 298
            logger.info("Using default temperature of 298 K")
        bead_dict = dict_dimensions(bead_dict0.copy(), temperature, dimensions=False)
    else:
        bead_dict = bead_dict0.copy()

    if sigma0 is None:
        if lower_bound == "rmin":
            rm = mie_potential_minimum(bead_dict)
        elif lower_bound == "sigma":
            rm = bead_dict["sigma"]
    else:
        rm = float_dimensions(sigma0,"sigma",temperature,dimensions=False)

    a = -2 / bead_dict['ionization_energy'] * (bead_dict['charge']**2. * rm**2 + 2 * bead_dict['dipole']**2 / 3 +
                                               3 * bead_dict['quadrupole']**2.0 * rm**2)
    b = 4 / bead_dict['ionization_energy']**2 * (
        bead_dict['charge']**4. * rm**4 + 4 * bead_dict['charge']**2. * bead_dict['dipole']**2 * rm**2 / 3 +
        6 * bead_dict['quadrupole']**2. * bead_dict['charge']**2. / 5 + 4 / 9 * bead_dict['dipole']**4 + 4 / 5 *
        bead_dict['dipole']**2 * bead_dict['quadrupole']**2.0 / rm**2 + 9 / 25 * bead_dict['quadrupole']**4.0 / rm**4)
    c = 4 / bead_dict['ionization_energy'] * (
        bead_dict['charge']**2. * bead_dict['dipole']**2 * rm**2 + bead_dict['dipole']**4 / 3 +
        bead_dict['quadrupole']**2. * bead_dict['charge']**2. / 5 +
        3 / 5 * bead_dict['quadrupole']**2. * bead_dict['dipole']**2. / rm**2 +
        3 / 5 * bead_dict['quadrupole']**4.0 / rm**4 - prefactor(bead_dict['lambdar'], bead_dict['lambdaa']) /
        (bead_dict['lambdaa'] - 3) * bead_dict['epsilon'] * bead_dict['sigma']**bead_dict['lambdaa'] / rm**
        (bead_dict['lambdaa'] - 6))

    partial_dict = {}
    for key in bead_dict0:
        if key == "ionization_energy":
            partial_dict[key] = -(a + np.sqrt(b - c)) / bead_dict['ionization_energy']
        elif key == "charge":
            tmp1 = 4 / bead_dict['ionization_energy']**2 * (
                4 * bead_dict['charge']**3 * rm**4 + 8 / 3 * bead_dict['charge'] * bead_dict['dipole']**2 * rm**2 +
                bead_dict['charge'] * bead_dict['quadrupole']**2 * 12 / 5)
            tmp2 = 8 / bead_dict['ionization_energy'] * (bead_dict['charge'] * bead_dict['dipole']**2 * rm**2 +
                                                         bead_dict['charge'] * bead_dict['quadrupole']**2 / 5)
            partial_dict[key] = -4 * bead_dict['charge'] * rm**2 / bead_dict['ionization_energy'] + (tmp1 - tmp2) / (
                2 * np.sqrt(b - c))
        elif key == "dipole":
            tmp1 = 4 / bead_dict['ionization_energy']**2 * (
                8 / 3 * bead_dict['charge']**2 * rm**2 * bead_dict['dipole'] + 16 / 9 * bead_dict['dipole']**3 +
                8 / 5 * bead_dict['dipole'] * bead_dict['quadrupole']**2 / rm**2)
            tmp2 = 8 / bead_dict['ionization_energy'] * (
                bead_dict['charge'] * bead_dict['dipole']**2 * rm**2 + 4 / 3 * bead_dict['dipole']**3 +
                3 / 5 * bead_dict['dipole'] * bead_dict['quadrupole']**2 / rm**2)
            partial_dict[key] = -8 / 3 * bead_dict['dipole'] / bead_dict['ionization_energy'] + (tmp1 - tmp2) / (
                2 * np.sqrt(b - c))
        elif key == "quadrupole":
            tmp1 = 4 / bead_dict['ionization_energy']**2 * (12 / 5 * bead_dict['charge']**2 * bead_dict['quadrupole'] +
                                                            8 / 5 * bead_dict['dipole']**2 * bead_dict['quadrupole'] /
                                                            rm**2 + 36 / 25 * bead_dict['quadrupole']**3 / rm**4)
            tmp2 = 4 / bead_dict['ionization_energy'] * (2 / 5 * bead_dict['charge']**2 * bead_dict['quadrupole'] + 6 /
                                                         5 * bead_dict['dipole']**2 * bead_dict['quadrupole'] / rm**2 +
                                                         12 / 5 * bead_dict['quadrupole']**3 / rm**4)
            partial_dict[key] = -12 / 5 * bead_dict['quadrupole'] / bead_dict['ionization_energy'] / rm**2 + (
                tmp1 - tmp2) / (2 * np.sqrt(b - c))

    if not nondimensional:
        for key in partial_dict:
            if key != "charge":
                tmp = float_dimensions(partial_dict[key], key, temperature, dimensions=True)
            else:
                tmp = partial_dict[key]
            partial_dict[key] = float_dimensions(tmp, "polarizability", temperature)

    return partial_dict


def partial_energy_parameter(beadA,
                             beadB,
                             temperature=None,
                             nondimensional=False,
                             lower_bound="rmin",
                             distance_opts={},
                             polarizability_opts={},
                             shape_factor_scale=False,
                             sigma0=None):
    r"""
    Calculate partial derivative with respect to multipole moments. This is useful in estimating the error.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    distance_opts : dict, Optional, default={}
        Dictionary of keyword arguments for :func:`~mapsci.multipole_mie_combining_rules.calc_distance_array`
    temperature : float, Optional, default=298
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    sigma0 : float, Optional, default=None
        This lower bound of the integral dictates where the lower bound of the definite integral is. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    polarizability_opts : dict, Optional, default={}
        Dictionary of keyword arguments used in :func:`~mapsci.multipole_mie_combining_rules.calc_polarizability`
    lower_bound : str, Optional, default='rmin'
        Lower bound of distance array. Can be one of:

        - rmin: the position of the potential well
        - sigma: the size parameter
    
    Returns
    -------
    partial_dict : dict
        Partial derivative with respect to multipole moments
    """

    if not nondimensional:
        if temperature is None:
            temperature = 298
            logger.info("Using default temperature of 298 K")
        bead1 = dict_dimensions(beadA.copy(), temperature, dimensions=False)
        bead2 = dict_dimensions(beadB.copy(), temperature, dimensions=False)
    else:
        bead1 = beadA.copy()
        bead2 = beadB.copy()

    bead_dict = {"0": bead1, "1": bead2}
    polarizability_opts.update({"shape_factor_scale":shape_factor_scale})
    bead_dict = calc_polarizability(bead_dict,
                                    distance_opts=distance_opts,
                                    calculation_method="analytical",
                                    polarizability_opts=polarizability_opts,
                                    nondimensional=True)

    beadAB = mie_combining_rules(bead1, bead2)

    if sigma0 is None:
        if lower_bound == "rmin":
            rm = mie_potential_minimum(beadAB)
        elif lower_bound == "sigma":
            rm = beadAB["sigma"]
    else:
        rm = float_dimensions(sigma0,"sigma",temperature,dimensions=False)

    tmp = prefactor(beadAB["lambdar"],
                    beadAB["lambdaa"]) / (beadAB["lambdaa"] - 3) * beadAB["sigma"]**beadAB["lambdaa"] / rm**(beadAB["lambdaa"] - 3)

    if shape_factor_scale:
        tmp = tmp * beadA["Sk"] * beadB["Sk"]

    partial_dict = {"0": {}, "1": {}}
    for i in [0, 1]:
        key1 = str(1 * i)
        key2 = str(1 - i)

        for key in bead_dict[key1]:
            if key == "ionization_energy":
                I = bead_dict[key2]['ionization_energy']**2 / (bead_dict[key1]['ionization_energy'] +
                                                               bead_dict[key2]['ionization_energy'])**2
                partial_dict[key1][
                    key] = bead_dict[key1]['polarizability'] * bead_dict[key2]['polarizability'] / rm**3 / 2 / tmp
            elif key == "charge":
                tmp1 = bead_dict[key1]['charge'] / rm * (bead_dict[key2]['polarizability'] +
                                                         bead_dict[key2]['dipole']**2)
                tmp2 = bead_dict[key1]['charge'] * bead_dict[key2]['quadrupole']**2 / rm**3 / 10
                partial_dict[key1][key] = (tmp1 + tmp2) / tmp
            elif key == "dipole":
                tmp1 = bead_dict[key2]['charge']**2 * bead_dict[key1]['dipole'] / rm
                tmp2 = 2 / 3 * bead_dict[key1]['dipole'] / rm**3 * (bead_dict[key2]['dipole']**2 +
                                                                    bead_dict[key2]['polarizability'])
                tmp3 = 3 / 5 / rm**5 * bead_dict[key1]['dipole'] * bead_dict[key2]['quadrupole']**2
                partial_dict[key1][key] = (tmp1 + tmp2 + tmp3) / tmp
            elif key == "quadrupole":
                tmp1 = bead_dict[key2]['charge']**2 * bead_dict[key1]['quadrupole'] / rm**3 / 5
                tmp2 = 3 / 5 * bead_dict[key1]['quadrupole'] / rm**5 * (bead_dict[key2]['dipole']**2 +
                                                                        bead_dict[key2]['polarizability'])
                tmp3 = 6 / 5 / rm**7 * bead_dict[key1]['quadrupole'] * bead_dict[key2]['quadrupole']**2
                partial_dict[key1][key] = (tmp1 + tmp2 + tmp3) / tmp
            elif key == "polarizability":
                I = bead_dict[key1]['ionization_energy'] * bead_dict[key2]['ionization_energy'] / (
                    bead_dict[key1]['ionization_energy'] + bead_dict[key2]['ionization_energy'])
                tmp1 = bead_dict[key2]['charge']**2 / rm / 2
                tmp2 = 1 / 3 / rm**3 * (bead_dict[key2]['dipole']**2 + 3 / 2 * bead_dict[key2]['polarizability'] * I)
                tmp3 = 3 / 10 / rm**5 * bead_dict[key2]['quadrupole']**2
                partial_dict[key1][key] = (tmp1 + tmp2 + tmp3) / tmp

            if not nondimensional:
                for key in partial_dict[key1]:
                    if key != "charge":
                        tmp1 = float_dimensions(partial_dict[key1][key], key, temperature, dimensions=True)
                    else:
                        tmp1 = partial_dict[key1][key]
                    partial_dict[key1][key] = float_dimensions(tmp1, "epsilon", temperature)

    return partial_dict


def multipole_integral(beadA, beadB, sigma0=None, lower_bound="rmin", multipole_terms=None, temperature=None, nondimensional=False):
    r"""
    Calculate the integral of the multipole potential from a given minimum to infinity. Units in those of :math:`\epsilon/\sigma^3`

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor
    sigma0 : float, Optional, default=None
        This lower bound of the integral dictates where we expect to start matching the multipole attractive term with that of Mie potential. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`. If None, the value taken from 'lower_bound' will be used
    lower_bound : str, Optional, default='rmin'
        Lower bound of distance array. Can be one of:

        - rmin: the position of the potential well
        - sigma: the size parameter

    multipole_terms : numpy.ndarray, Optional, default=None
        This list of terms corresponds to the coefficients for r to the order of -4, -6, -8, and -10, respectively. If not provided, this quantity will be calculated. These are ALWAYS dimensionless
    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`

    Returns
    -------
    Cmultipole : float
        Sum of integral terms. Either in [kcal/mol] or dimensionless :math:`C_{multi}'=C_{multi}/(3k_{B}T)`
    multipole_int_terms : numpy.ndarray
        This list of terms corresponds to the terms involved in calculation of the energy parameter, epsilon. These terms sum to equal epsilon. Either in [kcal/mol] or dimensionless :math:`C_{multi}'=C_{multi}/(3k_{B}T)`

    """

    if lower_bound == None and sigma0 == None:
        raise ValueError("Either a lower bound for integration must be provided with the keyword 'sigma0', or specified with 'lower_bound'")

    if not nondimensional:
        if temperature is None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead1 = dict_dimensions(beadA.copy(), temperature, dimensions=False)
        bead2 = dict_dimensions(beadB.copy(), temperature, dimensions=False)
        if sigma0 != None:
            sigma0 = float_dimensions(sigma0, "sigma", temperature, dimensions=False)
    else:
        bead1 = beadA.copy()
        bead2 = beadB.copy()

    if sigma0 == None:
        bead_dict = mie_combining_rules(bead1, bead2)
        if lower_bound == "rmin":
            sigma0 = mie_potential_minimum(bead_dict)
        elif lower_bound == "sigma":
            sigma0 = bead_dict["sigma"]

    if multipole_terms is None:
        multipole_terms = calc_cross_multipole_terms(bead1, bead2, nondimensional=True)

    if np.size(multipole_terms) == 4:
        integral = -4 * np.pi * np.array([sigma0**(-1), sigma0**(-3) / 3, sigma0**(-5) / 5, sigma0**(-7) / 7])
    elif np.size(multipole_terms) == 9:
        integral = -4 * np.pi * np.array([
            sigma0**(-1), sigma0**(-1), sigma0**(-3) / 3, sigma0**(-3) / 3, sigma0**(-3) / 3, sigma0**(-3) / 3,
            sigma0**(-5) / 5, sigma0**(-5) / 5, sigma0**(-7) / 7
        ])
    else:
        raise ValueError(
            "Multipole terms input should be either of length 4 or length 9 for the supported interaction types.")

    multipole_int_terms0 = integral * multipole_terms
    Cmultipole = np.sum(multipole_int_terms0)

    if not nondimensional:
        for tmp in ["epsilon", "sigma", "sigma", "sigma"]:
            Cmultipole = float_dimensions(Cmultipole,tmp,temperature,dimensions=True)
            multipole_int_terms0 = float_dimensions(multipole_int_terms0,tmp,temperature,dimensions=True)

    return Cmultipole, multipole_int_terms0


def solve_multipole_cross_interaction_integral(sigma0,
                                               beadA,
                                               beadB,
                                               multipole_terms=None,
                                               shape_factor_scale=False,
                                               temperature=None,
                                               nondimensional=False,
                                               beadAB=None):
    r"""
    Calculation of nondimensionalized cross-interaction potential from multipole moments.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    sigma0 : float
        This lower bound of the integral dictates where we expect to start matching the multipole attractive term with that of Mie potential. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    beadA : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    beadB : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    multipole_terms : numpy.ndarray, Optional, default=None
        This list of terms corresponds to the coefficients for r to the order of -4, -6, -8, and -10, respectively. If not provided, this quantity will be calculated. These are ALWAYS nondimensionalized
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    beadAB : dict
        Dictionary of mixed Mie parameters for beadA and beadB.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    
    Returns
    -------
    epsilon : float
        Cross interaction parameter from analytical solution of extended combining rules. Array is equal in length to "r". Either in reduced units :math:`C_{multi}'=C_{multi}/k_{B}` or dimensionless :math:`C_{multi}'=C_{multi}/(3k_{B}T)`
    multipole_int_terms : numpy.ndarray
        This list of terms corresponds to the terms involved in calculation of the energy parameter, epsilon. Adding these terms together produces the attractive term of the Mie potential, from which the energy parameter can be derived. Always dimensionless :math:`C_{multi}'=C_{multi}/(3k_{B}T)`
    """

    if not nondimensional:
        if temperature is None:
            logger.error("Temperature should be included when 'nondimensional' is False")
        bead1 = dict_dimensions(beadA.copy(), temperature, dimensions=False)
        bead2 = dict_dimensions(beadB.copy(), temperature, dimensions=False)
        sigma0 = float_dimensions(sigma0,"sigma",temperature,dimensions=False)
    else:
        bead1 = beadA.copy()
        bead2 = beadB.copy()

    if beadAB is None:
        beadAB_new = mie_combining_rules(bead1, bead2)
    else:
        if not nondimensional:
            beadAB_new = dict_dimensions(beadAB.copy(), temperature, dimensions=False)
        else:
            beadAB_new = beadAB.copy()

    eps_tmp = beadAB_new["epsilon"]

    Cmultipole, multipole_int_terms0 = multipole_integral(bead1, bead2, sigma0=sigma0, multipole_terms=multipole_terms, nondimensional=True)

    eps_min = eps_tmp / 20
    eps_max = eps_tmp * 2

    epsilon = spo.brentq(_obj_energy_parameter_from_integral,
                         eps_min,
                         eps_max,
                         args=(bead1, bead2, beadAB_new, Cmultipole, sigma0, shape_factor_scale),
                         xtol=1e-12)

    if not nondimensional:
        epsilon = float_dimensions(epsilon,"epsilon",temperature,dimensions=True)

    return epsilon, multipole_int_terms0

def _obj_energy_parameter_from_integral(eps0, beadA, beadB, beadAB, Cintegral, sigma0, shape_factor_scale=False):
    r"""
    Objective function used to fit energy parameter to integral of multipole moment

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    epsilon : float
        Guess in nondimensionalized energy parameter in [kcal/mol], :math:`\epsilon'=\epsilon/(3k_{B}T)`
    bead1 : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    bead2 : dict
        Dictionary of multipole parameters for bead_B.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    beadAB : dict
        Dictionary of mixed Mie parameters for bead1 and bead2.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    Cintegral : float
        This sum of the multipole integrals is set equal to the attractive term of the integrated Mie potential to determine the energy parameter.
    sigma0 : float
        The lower bound of the integral, can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj

    Returns
    -------
    obj_value : float
        Difference between multipole term and Mie potential term integral
    """

    Cint = mie_integral(beadAB, sigma0=sigma0, shape_factor_scale=shape_factor_scale)

    return eps0 * Cint / beadAB["epsilon"] - Cintegral


def mie_integral(beadAB, sigma0=None, lower_bound="rmin", shape_factor_scale=False):
    r"""
    Calculate the integral of the attractive term in the Mie potential from the given minimum value to infinity. Units in those of :math:`\epsilon/\sigma^3`

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    beadAB : dict
        Dictionary of mixed Mie parameters for bead1 and bead2.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent

    sigma0 : float, Optional, default=None
        This lower bound of the integral dictates where we expect to start matching the multipole attractive term with that of Mie potential. Can be reported in [Å] or nondimensionalized as :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`. If None, the value taken from 'lower_bound' will be used
    lower_bound : str, Optional, default='rmin'
        Lower bound of distance array. Can be one of:

        - rmin: the position of the potential well
        - sigma: the size parameter

    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj

    Returns
    -------
    Cintegral : float
        Value of the definite Mie integral from sigma0 to infinity
    """

    if lower_bound == None and sigma0 == None:
        raise ValueError("Either a lower bound for integration must be provided with the keyword 'sigma0', or specified with 'lower_bound'")

    if sigma0 == None:
        if lower_bound == "rmin":
            sigma0 = mie_potential_minimum(beadAB)
        elif lower_bound == "sigma":
            sigma0 = beadAB["sigma"]

    if shape_factor_scale:
        if "Sk" in beadAB:
            beadAB["epsilon"] = beadAB["epsilon"] * beadAB["Sk"]**2
        else:
            raise ValueError("Shape factor was not provided in bead dictionary")

    integral = -4 * np.pi * beadAB["epsilon"] * prefactor(
        beadAB["lambdar"],
        beadAB["lambdaa"]) * beadAB["sigma"]**beadAB["lambdaa"] / sigma0**(beadAB["lambdaa"] - 3) / (beadAB["lambdaa"] - 3)

    return integral

def fit_multipole_cross_interaction_parameter(beadA,
                                              beadB,
                                              distance_opts={},
                                              distance_array=None,
                                              shape_factor_scale=False,
                                              nondimensional=False,
                                              temperature=None):
    r"""
    Calculation of nondimensionalized cross-interaction parameter for the Mie potential.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    beadA : dict
        Dictionary of Mie and multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    beadB : dict
        Dictionary of Mie and multipole parameters for bead_B.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    temperature : float, Optional, default=None
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    distance_opts : dict, Optional, default={}
        Dictionary of keyword arguments for :func:`~mapsci.multipole_mie_combining_rules.calc_distance_array`
    distance_array : numpy.ndarray, Optional, default=None
        Array (or float) in either [Å] or nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`, whatever is consistent with 'bead_dict'. If None, 'distance_opts' are used to generate the array.

    Returns
    -------
    output_dict : dict
        Dictionary of:

        - epsilon (float) Fit energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`. Calculated from fit lambda and van der Waals attraction parameter.
        - kij (float) Binary interaction parameter for fit energy parameter, where :math:`\epsilon_{fit}=(1-k_{ij})\sqrt{\epsilon_i\epsilon_j}`
        - sigma (float) Size parameter taken at mean, reported in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Fit repulsive exponent, calculated as K/epsilon_fit
        - lambdaa (float) Fit attractive exponent
        - lambdaa_variance (float) Variance in attractive exponent during fitting process
        - epsilon_saft (float) Energy parameter from SAFT method of scaling with geometric mean, scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - kij (float) Binary interaction parameter for SAFT prediction of energy parameter, where epsilon_saft = :math:`\epsilon_{saft}=(1-k_{ij,saft})\sqrt{\epsilon_i\epsilon_j}`
        - K (float) Equal to :math:`C_{Mie}\epsilon_{fit}`, used in fitting process. Used to calculate lambdar.
        - K_variance (float) Variance in calculation of dummy variable K

    """

    if not nondimensional:
        if temperature is None:
            logger.error("Temperature should be included with 'nondimensional' is False")
        bead1 = dict_dimensions(beadA.copy(), temperature, dimensions=False)
        bead2 = dict_dimensions(beadB.copy(), temperature, dimensions=False)
    else:
        bead1 = beadA.copy()
        bead2 = beadB.copy()

    # Set-up Mie parameters
    beadAB = mie_combining_rules(bead1, bead2)
    Cmie = prefactor(beadAB["lambdar"], beadAB["lambdaa"])
    if shape_factor_scale:
        if "Sk" not in beadA:
            beadA["Sk"] = 1.0
        if "Sk" not in beadB:
            beadB["Sk"] = 1.0

    multipole_terms = calc_cross_multipole_terms(bead1, bead2, nondimensional=True)

    # From curve fit
    if distance_array is None:
        r = calc_distance_array(beadAB, **distance_opts)
    else:
        r = distance_array

    w_multipole, potential_terms = calc_cross_multipole_potential(r, multipole_terms, total_only=False, nondimensional=True)

    # ___________ VDW parameter combining _______________
    params, var_matrix = spo.curve_fit(lambda x, K, lambdaa: log_mie_attractive(
        r, bead1, bead2, lambda_a=lambdaa, Kprefactor=K, shape_factor_scale=shape_factor_scale),
                                       r,
                                       np.log(-w_multipole),
                                       p0=[beadAB["epsilon"] * Cmie, beadAB["lambdaa"]],
                                       bounds=(0.0, np.inf))
    K = params[0]
    lambdaa_fit = params[1]
    eps_fit = calc_epsilonij_from_lambda_aij(lambdaa_fit, bead1, bead2)
    if K / eps_fit < 1.01:
        raise ValueError(
            "A suitable repulsive exponent cannot be calculated using the following cross interaction parameters:\n    epsilon: {}, lambdaa: {}, Cmie: {} < 1.0\n    Check self-interaction parameters above. A common cause could be poorly fit polarizability because a partial charge was assigned to an bead where it's Mie potential is fit to expect dipole to be the highest order."
            .format(float_dimensions(eps_fit, "epsilon", temperature), lambdaa_fit, K / eps_fit))
    else:
        try:
            lambdar_fit = spo.brentq(lambda x: K / eps_fit - prefactor(x, lambdaa_fit), lambdaa_fit * 1.01, 1e+4, xtol=1e-12)
        except:
            raise ValueError("This shouldn't happen, check given parameters.")

    # Save output
    if not nondimensional:
        tmp = beadAB["epsilon"] * np.sqrt(bead1["sigma"]**3 * bead2["sigma"]**3) / beadAB["sigma"]**3
        beadAB["epsilon_saft"] = float_dimensions(tmp,"epsilon",temperature,dimensions=True)
        beadAB["epsilon"] = float_dimensions(eps_fit,"epsilon",temperature,dimensions=True)
        beadAB["K"] = float_dimensions(K,"epsilon",temperature,dimensions=True)
        beadAB["K_variance"] = float_dimensions(var_matrix[1][1],"epsilon",temperature,dimensions=True)
        beadAB["sigma"] = float_dimensions(beadAB["sigma"],"sigma",temperature,dimensions=True)
    else:
        beadAB["epsilon_saft"] = beadAB["epsilon"] * np.sqrt(
            bead1["sigma"]**3 * bead2["sigma"]**3) / beadAB["sigma"]**3
        beadAB["epsilon"] = eps_fit
        beadAB["K"] = K
        beadAB["K_variance"] = var_matrix[1][1]

    beadAB["lambdaa"] = lambdaa_fit
    beadAB["lambdaa_variance"] = var_matrix[0][0]
    beadAB["lambdar"] = lambdar_fit
    beadAB["kij_saft"] = 1 - beadAB["epsilon_saft"] / np.sqrt(bead1["epsilon"]*bead2["epsilon"])
    beadAB["kij"] = 1 - beadAB["epsilon"] / np.sqrt(bead1["epsilon"]*bead2["epsilon"])

    return beadAB

def log_mie_attractive(r, bead1, bead2, lambda_a=None, Kprefactor=None, epsilon=None, shape_factor_scale=False):
    r"""
    Calculate the log of the attractive term of the Mie potential. This linearizes the curve for the fitting process

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.

    Parameters
    ----------
    r : numpy.ndarray
        Array (or float) of nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
    bead1 : dict
        Dictionary of multipole parameters for bead_A.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    bead2 : dict
        Dictionary of multipole parameters for bead_B. If provided, the mixed energy parameter is fit.

        - epsilon (float) Nondimensionalized energy parameter, :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalized size parameter, :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - Sk (float) Shape factor

    epsilon : float, Optional, default=None
        The energy parameter for the Mie potential, if not specified the combining rule from `Lafitte 2013 <https://doi.org/10.1063/1.4819786>`_ is used
    lambda_a : float, Optional, default=None
        The cross interaction attractive exponent, if not specified the combining rule from `Lafitte 2013 <https://doi.org/10.1063/1.4819786>`_ is used
    Kprefactor : float, Optional, default=None
        Total prefactor of Mie potential equal to the energy parameters times the Mie prefactor, C. If not specified, the value using the combining rules from `Lafitte 2013 <https://doi.org/10.1063/1.4819786>`_ is used.
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj

    Returns
    -------
    log_potential : numpy.ndarray
        The potential array for the given value of epsilon
    """

    beadAB = mie_combining_rules(bead1, bead2)
    sigma = beadAB["sigma"]
    lambda_r = beadAB["lambdar"]

    if epsilon is not None and lambda_a is not None:
        # Assume lambdar follows normal combining rules
        Kprefactor = epsilon * prefactor(lambda_r, lambda_a)
    elif epsilon is not None and Kprefactor is not None:
        raise ValueError("Specifying 'epsilon' and 'Kprefactor' is redundant.")
    elif epsilon is not None:
        # Assume both exponents follow normal combining rules
        lambda_a = beadAB["lambdaa"]
        Kprefactor = epsilon * prefactor(lambda_r, lambda_a)
    elif lambda_a is not None and Kprefactor is None:
        # Assume lambdar follows normal combining rules, epsilon can be derived from 1 fluid combining rule
        epsilon = calc_epsilonij_from_lambda_aij(lambda_a, bead1, bead2)
        Kprefactor = epsilon * prefactor(lambda_r, lambda_a)
    elif lambda_a is None and Kprefactor is not None:
        # Assume lambdaa follows normal combining rules
        lambda_a = beadAB["lambdaa"]

    if shape_factor_scale:
        Kprefactor = Kprefactor * bead1["Sk"] * bead2["Sk"]

    return np.log(Kprefactor) + lambda_a * np.log(sigma / r)


def calc_self_mie_from_multipole(bead_dict,
                                 mie_vdw=None,
                                 temperature=298,
                                 lambda_r=12,
                                 distance_opts={},
                                 distance_array=None,
                                 polarizability_opts={},
                                 shape_factor_scale=False,
                                 nondimensional=False):
    r"""
    Calculation of self-interaction parameters for the Mie potential from multipole moments.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    bead_dict : dict
        Dictionary of Mie and multipole parameters for bead_A.

        - epsilon (float) Energy parameter scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Size parameter in [Å], or nondimensionalized as :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - charge (float) Charge of bead in [e], or nondimensionalized as :math:`q'=q/e`
        - dipole (float) Dipole of bead in [Debye], or nondimensionalized as :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Quadrupole of bead in [Debye*Å], or nondimensionalized as :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Ionization_energy of bead in [kcal/mol], or nondimensionalized as :math:`I'=I/(3k_{B}T)`
        - polarizability (float) Polarizability of bead in [:math:`Å^3`] or nondimensionalized with :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume

    mie_vdw : float, Optional, default=None
        This nondimensionalized attractive parameter for the Mie potential is related not only to the Mie exponents but also to the triple and critical temperatures of a substance. It can be used to specify the repulsive exponent, otherwise a value of 12 is assumed
    lambda_r : float, Optional, default=12
        Assumed repulsive exponent. This quantity can be changed later as long as the energy parameter is scaled accordingly.
    temperature : float, Optional, default=298
        Temperature in [K] for adding and removing dimensions, if the parameters are nondimensionalized, this value isn't used.
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    distance_opts : dict, Optional, default={}
        Optional keywords for creating r array used for calculation or fitting 
    polarizability_opts : dict, Optional, default={}
        Dictionary of keyword arguments for :func:`~mapsci.multipole_mie_combining_rules.fit_polarizability` or :func:`~mapsci.multipole_mie_combining_rules.solve_polarizability_integral`
    nondimensional : bool, Optional, default=False
        Indicates whether the given bead library has been nondimensionalized by :func:`~mapsci.multipole_mie_combining_rules.dict_dimensions`
    distance_array : numpy.ndarray, Optional, default=None
        Array (or float) in either [Å] or nondimensionalized distance between two beads. :math:`r'=r (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`, whatever is consistent with 'bead_dict'. If None, 'distance_opts' are used to generate the array.

    Returns
    -------
    cross_dict : dict
        Dictionary with energy parameter and exponents for Mie cross interaction between the given beads.

        - epsilon (float) Fit energy parameter, scaled by :math:`k_{B}` in [K], or nondimensionalized as :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - lambdar (float) Repulsive exponent, if mie_vdw is provided, otherwise this is the same value that was given.
        - lambdaa (float) Fit attractive exponent

    """

    if not nondimensional:
        logger.info("Calculating cross-interaction parameter with temperature of {}.".format(temperature))
        bead_dict_new = dict_dimensions(bead_dict.copy(), temperature, dimensions=False)
    else:
        bead_dict_new = bead_dict.copy()

    if shape_factor_scale:
        if "Sk" not in bead_dict_new:
            bead_dict_new["Sk"] = 1.0

    if "polarizability" not in bead_dict_new:
        logger.debug("Calculating polarizability")
        polarizability_opts.update({"shape_factor_scale":shape_factor_scale})
        bead_dict_new = calc_polarizability(bead_dict_new, distance_opts=distance_opts, calculation_method="fit", polarizability_opts=polarizability_opts, nondimensional=True)

    multipole_terms = calc_cross_multipole_terms(bead_dict_new, bead_dict_new, nondimensional=True)
    if distance_array is None:
        r = calc_distance_array(bead_dict_new, **distance_opts)
    else:
        r = distance_array
    w_multipole, potential_terms = calc_cross_multipole_potential(r, multipole_terms, total_only=False, nondimensional=True)

    Cmie = prefactor(bead_dict_new["lambdar"], bead_dict_new["lambdaa"])
    params, var_matrix = spo.curve_fit(lambda x, K, lambdaa: log_mie_attractive(
        r, bead_dict_new, bead_dict_new, lambda_a=lambdaa, Kprefactor=K, shape_factor_scale=shape_factor_scale),
                                       r,
                                       np.log(-w_multipole),
                                       p0=[bead_dict_new["epsilon"] * Cmie, bead_dict_new["lambdaa"]],
                                       bounds=(0.0, np.inf))
    K = params[0]
    bead_dict_new["lambdaa"] = params[1]
    if mie_vdw is not None:
        logger.info("Overwrite given lambdar with Mie potential relationship to vdW like parameter.")
        bead_dict_new["lambdar"] = calc_lambdarij_from_lambda_aij(bead_dict_new["lambdaa"], mie_vdw)

    if shape_factor_scale:
        bead_dict_new["epsilon"] = K / prefactor(bead_dict_new["lambdar"], bead_dict_new["lambdaa"]) / bead_dict_new["Sk"]**2
    else:
        bead_dict_new["epsilon"] = K / prefactor(bead_dict_new["lambdar"], bead_dict_new["lambdaa"])

    if not nondimensional:
        bead_dict_new = dict_dimensions(bead_dict_new, temperature, dimensions=True)

    return bead_dict_new

def extended_combining_rules_fitting(bead_library, temperature, shape_factor_scale=False, distance_opts={}, polarizability_opts={}):
    r"""
    Calculate and output the cross-interaction parameters for the provided dictionary of beads utilizing the Mie potential.

    Parameters
    ----------
    bead_library : dict
        Dictionary of dictionaries with Mie and multipole parameters for each bead in the desired system.

        - epsilon (float) [K] Energy parameter scaled by Boltzmann constant
        - sigma (float) [Å] Size parameter
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - polarizability (float) [:math:`Å^3`] This quantity is used as a free parameter in combining rule
        - charge (float) [-] Charge of bead fragment in elementary charges
        - dipole (float) [Debye] Dipole moment of bead fragment
        - quadrupole (float) [Debye*Å] Quadrupole moment of bead fragment
        - ionization_energy (float) [kcal/mol] Ionization energy of bead fragment

    temperature : float
        The temperature in [K] of the system
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    distance_opts : dict, Optional, default={}
        Optional keywords for creating r array used for calculation or fitting 
    polarizability_opts : dict, Optional, default={}
        Dictionary of keyword arguments used in :func:`~mapsci.multipole_mie_combining_rules.calc_polarizability`

    Returns
    -------
    cross_dict : dict
        Dictionary with "epsilon" value for cross interaction for the given beads.
    summary : dict
        Dictionary of bead types and details of their interactions with each of the other bead types. For each pair a dictionary entry is present for:

        - epsilon_saft (float) cross interaction with SAFT combining rules
        - kij_saft (float) binary interaction parameter for the energy parameter with SAFT combining rules
        - epsilon (float) cross interaction from multipole curve fit
        - kij (float) binary interaction parameter from multipole curve fit 
        - lambdar (float) repulsive exponent from multipole curve fit
        - lambdaa (float) attractive exponent from multipole curve fit
        - polarizability_* (float) polarizabilities for the two beads
    """

    bead_library_new = dict_dimensions(bead_library.copy(), temperature, dimensions=False)

    polarizability_opts.update({"shape_factor_scale":shape_factor_scale})
    bead_library_new = calc_polarizability(bead_library_new,
                                           distance_opts=distance_opts, 
                                           polarizability_opts=polarizability_opts,
                                           nondimensional=True)

    # Calculate cross interaction file
    dict_cross = {}
    dict_summary = {}
    beads = list(bead_library_new.keys())
    for i, bead1 in enumerate(beads):
        if len(beads[i + 1:]) > 0:
            dict_cross[bead1] = {}
            dict_summary[bead1] = {}
            for bead2 in beads[i + 1:]:

                cross_out = fit_multipole_cross_interaction_parameter(bead_library_new[bead1],
                                                                      bead_library_new[bead2],
                                                                      distance_opts=distance_opts,
                                                                      shape_factor_scale=shape_factor_scale,
                                                                      nondimensional=True,
                                                                      temperature=temperature)

                pol_i = float_dimensions(bead_library_new[bead1]["polarizability"], "polarizability", temperature)
                pol_j = float_dimensions(bead_library_new[bead2]["polarizability"], "polarizability", temperature)
                epsilon_saft = float_dimensions(cross_out["epsilon_saft"], "epsilon", temperature)
                epsilon_fit = float_dimensions(cross_out["epsilon"], "epsilon", temperature)

                dict_cross[bead1][bead2] = {
                    "epsilon": cross_out["epsilon"],
                    "lambdar": cross_out["lambdar"],
                    "lambdaa": cross_out["lambdaa"]
                }
                dict_summary[bead1][bead2] = {
                    "epsilon_saft": epsilon_saft,
                    "kij_saft":  cross_out["kij_saft"],
                    "epsilon": epsilon_fit,
                    "kij": cross_out["kij"],
                    "lambdar": cross_out["lambdar"],
                    "lambdaa": cross_out["lambdaa"],
                    "polarizability_"+bead1: pol_i,
                    "polarizability_"+bead2: pol_j,
                }

    dict_cross = dict_dimensions(dict_cross.copy(), temperature)

    return dict_cross, dict_summary


def extended_combining_rules_analytical(bead_library, temperature, shape_factor_scale=False, distance_opts={}, polarizability_opts={}):
    r"""
    Calculate and output the cross-interaction energy parameter for the provided dictionary of beads utilizing the Mie potential, using the Analytical (i.e. integral) method

    Parameters
    ----------
    bead_library : dict
        Dictionary of dictionaries with Mie and multipole parameters for each bead in the desired system.

        - epsilon (float) [K] Energy parameter scaled by Boltzmann constant
        - sigma (float) [Å] Size parameter
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - polarizability (float) [:math:`Å^3`] This quantity is used as a free parameter in combining rule
        - charge (float) [-] Charge of bead fragment in elementary charges
        - dipole (float) [Debye] Dipole moment of bead fragment
        - quadrupole (float) [Debye*Å] Quadrupole moment of bead fragment
        - ionization_energy (float) [kcal/mol] Ionization energy of bead fragment

    temperature : float
        The temperature in [K] of the system
    shape_factor_scale : bool, Optional, default=False
        Scale energy parameter based on shape factor epsilon*Si*Sj
    distance_opts : dict, Optional, default={}
        Optional keywords for creating r array used for calculation or fitting 
    polarizability_opts : dict, Optional, default={}
        Dictionary of keyword arguments used in :func:`~mapsci.multipole_mie_combining_rules.calc_polarizability`

    Returns
    -------
    cross_dict : dict
        Dictionary with `epsilon` value for cross interaction between given beads.
    summary : dict
        Dictionary of bead types and details of their interactions with each of the other bead types. For each pair a dictionary entry is present for:

        - epsilon_saft (float) cross interaction with SAFT combining rules
        - kij_saft (float) binary interaction parameter for the energy parameter with SAFT combining rules
        - epsilon (float) cross interaction from multipole analytical solution
        - kij (float) binary interaction parameter from multipole analytical solution
        - lambdar (float) repulsive exponent from SAFT combining rules
        - lambdaa (float) attractive exponent from SAFT combining rules
        - polarizability_* (float) polarizabilities for the two beads
    """

    if temperature == None or np.isnan(temperature):
        raise ValueError("Temperature must be a real number, given {}.".format(temperature))

    bead_library_new = dict_dimensions(bead_library.copy(), temperature, dimensions=False)

    polarizability_opts.update({"shape_factor_scale":shape_factor_scale})
    bead_library_new = calc_polarizability(bead_library_new,
                                           distance_opts=distance_opts,
                                           polarizability_opts=polarizability_opts,
                                           calculation_method="analytical",
                                           nondimensional=True)

    # Calculate cross interaction file
    dict_cross = {}
    dict_summary = {}
    beads = list(bead_library_new.keys())
    for i, bead1 in enumerate(beads):
        beadA = bead_library_new[bead1]
        if len(beads[i + 1:]) > 0:
            dict_cross[bead1] = {}
            dict_summary[bead1] = {}
            for bead2 in beads[i + 1:]:
                beadB = bead_library_new[bead2]
                beadAB = mie_combining_rules(beadA, beadB)
                r = calc_distance_array(beadAB, **distance_opts)
                epsilon_tmp, terms = solve_multipole_cross_interaction_integral(r[0],
                                                                                beadA,
                                                                                beadB,
                                                                                nondimensional=True,
                                                                                shape_factor_scale=shape_factor_scale)

                pol_i = float_dimensions(beadA["polarizability"], "polarizability", temperature)
                pol_j = float_dimensions(beadB["polarizability"], "polarizability", temperature)
                eps_saft_tmp = beadAB["epsilon"] * np.sqrt(beadA["sigma"]**3 * beadB["sigma"]**3) / beadAB["sigma"]**3
                epsilon_saft = float_dimensions(eps_saft_tmp, "epsilon", temperature)
                epsilon_analytical = float_dimensions(epsilon_tmp, "epsilon", temperature)
                kij_saft = 1 - eps_saft_tmp / beadAB["epsilon"]
                kij_analytical = 1 - epsilon_tmp / beadAB["epsilon"]

                dict_cross[bead1][bead2] = {"epsilon": epsilon_tmp}

                dict_summary[bead1][bead2] = {
                    "epsilon_saft": epsilon_saft,
                    "kij_saft":  kij_saft,
                    "epsilon": epsilon_analytical,
                    "kij": kij_analytical,
                    "lambdar": beadAB["lambdar"],
                    "lambdaa": beadAB["lambdaa"],
                    "polarizability_{}".format(bead1): pol_i,
                    "polarizability_{}".format(bead2): pol_j,
                }

    dict_cross = dict_dimensions(dict_cross.copy(), temperature)

    return dict_cross, dict_summary


def dict_dimensions(parameters, temperature, dimensions=True, conv_custom={}):
    r"""
    Obtain instructions for systems used in calculation.

    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    parameters : dict
        This dictionary of bead types contains a dictionary of parameters for each.

        - epsilon (float) Nondimensionalize energy parameter in [K], :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalize size parameter in [Å], :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - polarizability (float) Nondimensionalize polarizability of bead in [:math:`Å^3`]. :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
        - charge (float) Nondimensionalize charge of bead in [e]. :math:`q'=q/e`
        - dipole (float) Nondimensionalize dipole of bead in [Debye]. :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Nondimensionalize quadrupole of bead in [Debye*Å]. :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Nondimensionalize ionization_energy of bead in [kcal/mol]. :math:`I'=I/(3k_{B}T)`

    temperature : float
        The temperature of the system
    dimensions : bool, Optional, default=True
        If true, will add SI-units to multipole parameters, if False, will nondimensionalize. 
    conv_custom : dict, Optional, default={}
        This dictionary may have the same parameter names used for the beads and overwrite default values.

    Returns
    -------
    new_parameters : dict
        This dictionary of bead types contains a dictionary of parameters for each.
    """

    if temperature == None or np.isnan(temperature):
        raise ValueError("Temperature must be a real number, given {}.".format(temperature))

    # Nondimensionalize Parameters
    C_l = 1e+10  # [Ang/m]
    C_D = 3.33564e-20  # [C*Ang/Debye]
    C_e = 6.9477e-21  # [J / kcal/mol]
    C_eV = 1.602176565e-19  # [J/eV]
    e0 = 8.854187817e-12 * C_e / C_l  # [C^2/(J*m)] to [C^2*mol/(kcal*Ang)]
    kb = 1.38064852e-23 / C_e  # [J/K] to [kcal/(mol*K)] Boltzmann constant

    perm = (4 * np.pi * e0)**2  # [C^2*mol/(kcal*Ang)]^2
    K = 3 * kb * temperature  # [kcal/mol]

    conv = {"epsilon": 1/(3*temperature), \
            "ionization_energy": 1/K,
            "sigma": np.sqrt(perm)*K/C_eV**2, \
            "dipole": C_D*np.sqrt(perm)*K/C_eV**3, \
            "quadrupole": C_D*perm*K**2/C_eV**5, \
            "charge":1, \
            "polarizability": 4*np.pi*e0*perm*K**3/C_eV**6}
    #            "polarizability": perm*K**3/C_eV**6} Using the polarizability is in large units

    for key, value in conv_custom.items():
        conv[key] = value

    new_parameters = {}
    for k1, v1 in parameters.items():
        new_parameters[k1] = {}
        if type(v1) == dict:
            for k2, v2 in v1.items():
                if type(v2) == dict:
                    new_parameters[k1][k2] = {}
                    for k3, v3 in v2.items():
                        if k3 in conv:
                            if dimensions:
                                new_parameters[k1][k2][k3] = v3 / conv[k3]
                            else:
                                new_parameters[k1][k2][k3] = v3 * conv[k3]
                        else:
                            new_parameters[k1][k2][k3] = v3
                else:

                    if k2 in conv:
                        if dimensions:
                            new_parameters[k1][k2] = v2 / conv[k2]
                        else:
                            new_parameters[k1][k2] = v2 * conv[k2]
                    else:
                        new_parameters[k1][k2] = v2
        else:
            if k1 in conv:
                if dimensions:
                    new_parameters[k1] = v1 / conv[k1]
                else:
                    new_parameters[k1] = v1 * conv[k1]
            else:
                new_parameters[k1] = v1

    return new_parameters


def float_dimensions(parameter, parameter_type, temperature, dimensions=True, conv_custom={}):
    r"""
    Obtain instructions for systems used in calculation.
    
    Nondimensional parameters are scaled using the following physical constants: vacuum permittivity, :math:`\varepsilon_{0}`, Boltzmann constant, :math:`k_{B}`, and elementary charge, :math:`e`.
    
    Parameters
    ----------
    parameter : float
        Value of parameter to be converted.
    parameter_type : str
        Parameter name, can be:
    
        - epsilon (float) Nondimensionalize energy parameter in [K], :math:`\epsilon'=\epsilon/(3k_{B}T)`
        - sigma (float) Nondimensionalize size parameter in [Å], :math:`\sigma'=\sigma (4 \pi \varepsilon_{0}) 3k_{B}T e^{-2}`
        - lambdar (float) Repulsive exponent
        - lambdaa (float) Attractive exponent
        - polarizability (float) Nondimensionalize polarizability of bead in [:math:`Å^3`]. :math:`\alpha'=\alpha (4 \pi \varepsilon_{0}) 3k_{B}T  e^{-6}`, where the dimensionalized version is the polarizability volume
        - charge (float) Nondimensionalize charge of bead in [e]. :math:`q'=q/e`
        - dipole (float) Nondimensionalize dipole of bead in [Debye]. :math:`\mu'=\mu (4 \pi \varepsilon_{0}) 3k_{B}T e^{-3}`
        - quadrupole (float) Nondimensionalize quadrupole of bead in [Debye*Å]. :math:`Q'=Q (4 \pi \varepsilon_{0})^{2} (3k_{B}T)^{2} e^{-5}`
        - ionization_energy (float) Nondimensionalize ionization_energy of bead in [kcal/mol]. :math:`I'=I/(3k_{B}T)`
    
    temperature : float
        The temperature of the system
    dimensions : bool, Optional, default=True
        If true, will add SI-units to multipole parameters, if False, will nondimensionalize.
    conv_custom : dict, Optional, default={}
        This dictionary may have the same parameter names used for the beads and overwrite default values.
    
    Returns
    -------
    new_parameter : float
        Converted parameter
    """

    if temperature == None or np.isnan(temperature):
        raise ValueError("Temperature must be a real number, given {}.".format(temperature))

    # Nondimensionalize Parameters
    C_l = 1e+10  # [Ang/m]
    C_D = 3.33564e-20  # [C*Ang/Debye]
    C_e = 6.9477e-21  # [J / kcal/mol]
    C_eV = 1.602176565e-19  # [J/eV]
    e0 = 8.854187817e-12 * C_e / C_l  # [C^2/(J*m)] to [C^2*mol/(kcal*Ang)]
    kb = 1.38064852e-23 / C_e  # [J/K] to [kcal/(mol*K)] Boltzmann constant

    perm = (4 * np.pi * e0)**2  # [C^2*mol/(kcal*Ang)]^2
    K = 3 * kb * temperature  # [kcal/mol]

    conv = {"epsilon": 1/(3*temperature), \
            "ionization_energy": 1/K,
            "sigma": np.sqrt(perm)*K/C_eV**2, \
            "dipole": C_D*np.sqrt(perm)*K/C_eV**3, \
            "quadrupole": C_D*perm*K**2/C_eV**5, \
            "charge":1, \
            "polarizability": 4*np.pi*e0*perm*K**3/C_eV**6}

    for key, value in conv_custom.items():
        conv[key] = value

    if parameter_type in conv:
        if dimensions:
            new_parameter = parameter / conv[parameter_type]
        else:
            new_parameter = parameter * conv[parameter_type]
    else:
        raise KeyError("Parameter, {}, is not supported. Must be one of: {}".format(parameter_type, list(conv.keys())))

    return new_parameter


