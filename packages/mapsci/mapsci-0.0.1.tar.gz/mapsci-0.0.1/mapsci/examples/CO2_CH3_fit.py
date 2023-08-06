
import mapsci
import matplotlib.pyplot as plt



bead_library = {
    "CO2": {'epsilon': 353.55, 'sigma': 3.741, 'lambdar': 23.0, 'lambdaa': 6.66, 'Sk': 1.0, 'charge': 0.0, 'dipole': 0.0, 'quadrupole': 4.62033, 'ionization_energy': 316.3969563680995, 'mass': 0.04401},
    "CH3": {'epsilon': 256.77, 'sigma': 4.0773, 'lambdar': 15.05, 'lambdaa': 6.0, 'Sk': 0.57255, 'charge': -0.03278, 'dipole': 0.068168573, 'quadrupole': 0.060537996, 'ionization_energy': 254.80129735161324,'mass': 0.01503}
}
temperature = 273
keys = list(bead_library.keys())

mapsci.initiate_logger(log_file=True, verbose=10)
dict_cross, _ = mapsci.extended_combining_rules_fitting(bead_library, temperature, shape_factor_scale=True)

mapsci.plot_multipole_potential_from_dict(bead_library["CO2"], bead_library["CH3"], temperature=temperature, plot_terms=False, show=False)

# Plot mie potential with SAFT combining rules
mapsci.plot_attractive_mie_potential_from_dict(bead_library[keys[0]], 
                                               bead_library[keys[1]], 
                                               temperature=temperature, 
                                               plot_opts={"label": "SAFT"},
                                               show=False)
# Plot mie potential with Analytical method
mapsci.plot_attractive_mie_potential_from_dict(bead_library[keys[0]], 
                                               bead_library[keys[1]], 
                                               beadAB=dict_cross[keys[0]][keys[1]],
                                               temperature=temperature,
                                               plot_opts={"label": "Curve Fit"},
                                               show=False)

plt.legend(loc="best")
plt.show()

mapsci.initiate_logger(log_file=False, verbose=10)
