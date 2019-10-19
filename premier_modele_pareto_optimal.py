import numpy as np
import smartcity
import gym
import random
import scipy

env = gym.make("SmartCity-v1")

obs, info = env.reset()


alpha=1 # Happiness
beta=0 # Spendings
gamma=0 # Pollution

lights = np.array([1 for _ in range(obs["lights"].shape[0])])
heaters =  np.array([20 for _ in range(obs["heaters"].shape[0])]) 
energies = np.array([0.4*obs["needed_energy"],0.5*obs["needed_energy"], 0.1*obs["needed_energy"]])
actions = {"energies": energies, "heaters": heaters, "lights": lights}

obs, score, done, info = env.step(actions)

amount=obs['energies_amount']
needed_energy=obs['needed_energy']

prop=amount/needed_energy

def rennergy_score(proportions_energy):
    global obs
    lights = np.array([1 for _ in range(obs["lights"].shape[0])])
    heaters =  np.array([19 for _ in range(obs["heaters"].shape[0])]) 
    energies = np.array([proportions_energy[0]*obs["needed_energy"], proportions_energy[1]*obs["needed_energy"], proportions_energy[2]*obs["needed_energy"]])
    
    if np.sum(energies)<obs["needed_energy"]:
        return 10000
    actions = {"energies": energies, "heaters": heaters, "lights": lights}
    

    obs, score, done, info = env.step(actions)
    
    
    pollution=score["pollution"]*obs["needed_energy"]
    happiness=score["happiness"]
    spendings=np.dot(obs["energies_cost"],energies)
    return gamma*pollution - alpha*happiness + beta*spendings


liste_x0=[]
for _ in range(30):
    a=np.random.uniform(0,prop[0]-0.01)
    b=min(np.random.uniform(0,prop[1]-0.01),1-a)
    c=1-a-b
    liste_x0.append([a,b,c])

a=[ scipy.optimize.minimize(fun=rennergy_score, x0=liste_x0[i], bounds=[(0,prop[0]-0.01),(0,prop[1]-0.01),(0,prop[2]-0.01)] ,
                         constraints=scipy.optimize.LinearConstraint([1,1,1], 1.02, 2),options={'maxiter':100}) for i in range(30)]

a.sort(key=(lambda x: x["fun"]))
proportions_energy = a[0]['x']
lights = np.array([1 for _ in range(obs["lights"].shape[0])])
heaters =  np.array([19 for _ in range(obs["heaters"].shape[0])]) 
energies = np.array([proportions_energy[0]*obs["needed_energy"], proportions_energy[1]*obs["needed_energy"], proportions_energy[2]*obs["needed_energy"]])

if np.sum(energies)<obs["needed_energy"]:
    print('Nop')
else:
    actions = {"energies": energies, "heaters": heaters, "lights": lights}


obs, score, done, info = env.step(actions)

print(score)