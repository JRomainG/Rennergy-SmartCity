import numpy as np


def heaters_energy(heaters: np.array):
    """
    Return the energy used for the given temperature for the heaters
    """
    return heaters[heaters <= 18].sum() * 0.2 + \
           heaters[(18 < heaters) & (heaters <= 20)].sum() * 0.4 + \
           heaters[(20 < heaters) & (heaters <= 22)].sum() * 1.2 + \
           heaters[heaters > 22].sum() * 1.8


def lights_energy(lights: np.array):
    """
    Return the energy used for the given number of lights
    """
    return 0.1 * lights.sum()


def additional_consumption(prev_heaters: np.array, prev_lights: np.array,\
                           new_heaters: np.array, new_lights: np.array):
    """
    Return how much more energy will be needed (comparer to obs["needed_energy"])
    with the given lights and heaters settings
    """
    prev_heaters_energy = heaters_energy(prev_heaters)
    prev_lights_energy = heaters_energy(prev_lights)

    new_heaters_energy = heaters_energy(new_heaters)
    new_lights_energy = heaters_energy(new_lights)

    return new_heaters_energy + new_lights_energy - prev_heaters_energy - prev_lights_energy
