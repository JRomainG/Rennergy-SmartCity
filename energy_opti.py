from scipy.optimize import linprog
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

def main():
    # Visualisation optimum space

    val_count = 25
    alphas = np.linspace(0, 1, val_count)
    needed = np.linspace(30, 340, val_count)

    alphas_v, needed_v = np.meshgrid(alphas, needed, sparse=False, indexing='ij')

    # Default problem
    A = [100, 200, 30]
    C = [0.2, 0.5, 1]
    P = [1, 0, 0]
    # Custom
    # A = [100, 160, 80]
    # C = [0.2, 0.5, 1]
    # P = [1, 0.2, 0.8]

    results_e1 = np.zeros((val_count,val_count))
    results_e2 = np.zeros((val_count,val_count))
    results_e3 = np.zeros((val_count,val_count))
    for i, alpha in tqdm(enumerate(alphas), total=val_count):
        for j, n in enumerate(needed):
            # print(j)
            res = optimal_energy(alpha=alpha, needed=n, A=A, C=C, P=P)
            results_e1[i,j] = res[0]
            results_e2[i,j] = res[1]
            results_e3[i,j] = res[2]

    fig = plt.figure()
    ax = plt.axes(projection="3d")

    # alpha=0 : eco ballec
    # alpha=1 : 
    ax.plot_wireframe(alphas_v, needed_v, results_e1, 
        label='carbon', color='black', linewidths=0.7)
    ax.plot_wireframe(alphas_v, needed_v, results_e2, 
        label='nuke', color='purple', linewidths=0.7)
    ax.plot_wireframe(alphas_v, needed_v, results_e3, 
        label='renew', color='green', linewidths=0.7)
    # ax.plot_wireframe(alphas_v, needed_v, results_e1+results_e2+results_e3, 
        # label='energy sum', color='white', linewidths=0.5)
    ax.set_xlabel('ecology consideration ($\\alpha$ factor)')
    ax.set_ylabel('needed energy')
    ax.set_zlabel('energy quantity')
    plt.title('Optimal energy cocktails')
    plt.legend()
    plt.show()


def optimal_energy(
    alpha = 0.5,
    needed = 120,
    C = [0.2, 0.5, 1],
    P = [1, 0, 0],
    A = [100, 200, 30]):

    # TODO: change to take prefs into account

    # coeff_obj_i = (1-alpha)*c_i + alpha*p_i
    coeffs_obj = np.array(list(
        map(lambda tup: (1-alpha)*tup[0]+alpha*tup[1], zip(C, P))
    ))

    coeffs_prob = np.array([
        [-1, -1, -1],  # Reverse ineq cause x1+x2+x3 >= needed <=> -x1-x2-x3 <= -needed
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]])

    contraintes = np.array([-needed, *A])

    res = linprog(coeffs_obj, A_ub=coeffs_prob, b_ub=contraintes, bounds=[(0, None)]*3)
    return res.x.round(3)

if __name__ == '__main__':
    main()
