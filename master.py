import numpy as np
import smartcity
import gym
import energy


def main():
    # Init env
    env = gym.make("SmartCity-v0")
    obs, info = env.reset()

    # Deduce some parameters
    n_heaters = len(obs["heaters"])
    n_lights = len(obs["lights"])
    energy_available = obs["energies_amount"]
    energy_costs = obs["energies_cost"]

    print(f"Running simulation with {n_heaters} heaters and {n_lights} lights")
    print(f"Energy available: {energy_available}")
    print(f"Energy costs: {energy_costs}\n")

    # Run some steps
    print(f"----- Step 0 -----")
    print(f"Obs: {obs}")
    print(f"Info: {info}")

    for i in range(1, 11):
        # Turn all the lights on and put the heaters to 20°C
        lights = np.ones((n_lights,))
        heaters = 20 * np.ones((n_heaters,))

        # Compute the energy we need in total
        needed_energy = obs["needed_energy"]
        needed_energy += energy.additional_consumption(obs["heaters"], obs["lights"], heaters, lights)

        # Buy as much renewable as possible
        energies = np.zeros((3,))
        j = 3
        while needed_energy > 0 and j > 0:
            j -= 1
            energies[j] = min(needed_energy, energy_available[j])
            needed_energy -= energies[j]

        # Make sure we're not running out of energy
        assert needed_energy == 0

        # Do theses actions and proceed to the next step
        actions = {"energies": energies, "heaters": heaters, "lights": lights}
        obs, score, done, info = env.step(actions)

        # Print some logs
        print(f"Actions: {actions}")

        print(f"----- Step {i} -----")
        print(f"Obs: {obs}")
        print(f"Score: {score}")
        print(f"Info: {info}")


if __name__ == "__main__":
    main()
