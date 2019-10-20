import numpy as np
import smartcity
import gym
import random
import scipy

env = gym.make("SmartCity-v2")

obs, info = env.reset()


alpha=1 # Happiness
beta=0.003# Spendings
gamma=0.005 #Pollution

lights=[False]*(obs["lights"].shape[0])
nb_lamp_affected=np.array([0]*(info['light_interraction'].shape[0]))
nb_lamp_total=np.array([sum(info['light_interraction'][k,:]) for k in range(info['light_interraction'].shape[0])])
nb_user_total=[sum(info['light_interraction'][:,k]) for k in range(obs["lights"].shape[0])]
               
def can_i_turn_on_this_light_for_i(nb_lamp_affected,nb_lamp_total,light_i,info_light_interr):
    if all([info_light_interr[individu,light_i]==0 or nb_lamp_affected[individu]/nb_lamp_total[individu]<0.33 for individu in range(info['light_interraction'].shape[0])]):
        for individu in range(info['light_interraction'].shape[0]):
            if info_light_interr[individu,light_i]==1:
                nb_lamp_affected[individu]+=1
        return True
    return False
            


idxs = list(zip(*sorted([(val, i) for i, val in enumerate(nb_user_total)],reverse=True)))[1] 

for idx in idxs:
    if can_i_turn_on_this_light_for_i(nb_lamp_affected,nb_lamp_total,idx,info['light_interraction']):
        lights[idx]=True 

heaters =  np.array([0 for _ in range(obs["heaters"].shape[0])]) 
energies = np.array([0.4*obs["needed_energy"],0.5*obs["needed_energy"], 0.1*obs["needed_energy"]])
actions = {"energies": energies, "heaters": heaters, "lights": lights}

obs, score, done, info = env.step(actions)

amount=obs['energies_amount']
needed_energy=obs['needed_energy']

prop=amount/needed_energy

def rennergy_score(proportions_energy):
    global obs
    energies = np.array([proportions_energy[0]*obs["needed_energy"], proportions_energy[1]*obs["needed_energy"], proportions_energy[2]*obs["needed_energy"]])
    
    if np.sum(energies)<obs["needed_energy"]:
        return 10000
    actions = {"energies": energies, "heaters": heaters, "lights": lights}
    

    obs, score, done, info = env.step(actions)
    print(score)
    
    pollution=score["pollution"]*obs["needed_energy"]
    happiness=score["happiness"]
    spendings=np.dot(obs["energies_cost"],energies)
    return gamma*pollution - alpha*happiness + beta*spendings


liste_x0=[]
for _ in range(100):
    a=np.random.uniform(0,prop[0]-0.01)
    b=min(np.random.uniform(0,prop[1]-0.01),1-a)
    c=1-a-b
    liste_x0.append([a,b,c])

a=[ scipy.optimize.minimize(fun=rennergy_score, x0=liste_x0[i], bounds=[(0,prop[0]-0.01),(0,prop[1]-0.01),(0,prop[2]-0.01)] ,
                         constraints=scipy.optimize.LinearConstraint([1,1,1], 1.01, 2),options={'maxiter':30}) for i in range(100)]

a.sort(key=(lambda x: x["fun"]))
proportions_energy = a[0]['x'] 

while not done:
	energies = np.array([proportions_energy[0]*obs["needed_energy"], proportions_energy[1]*obs["needed_energy"], proportions_energy[2]*obs["needed_energy"]])

	if np.sum(energies)<obs["needed_energy"]:
	    print('Nop')
	else:
	    actions = {"energies": energies, "heaters": heaters, "lights": lights}


	obs, score, done, info = env.step(actions)
	print(score)