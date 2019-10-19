from scipy.optimize import linprog
import numpy as np

def optimal_energy(
    alpha = 0.5,
    needed = 120,
    C = [0.2, 0.5, 1],
    P = [1, 0, 0],
    A = [100, 200, 30]):

    # coeff_obj_i = (1-alpha)*c_i + alpha*p_i
    coeffs_obj = np.array(list(map(lambda tup: (1-alpha)*tup[0]+alpha*tup[1], zip(C, P))))

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
