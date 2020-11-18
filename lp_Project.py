import numpy as np 
from scipy import optimize

'''
coeffs of optimization are the weights multiplied by 
the square distances. Function takes in a list of 
distances and the assciated population list.
returns (1, k*n) array 

Maybe use a distionary for this
''' 

def get_coeffs(dist, pop):
	dist_arr = np.array(dist)
	pop_arr = np.array(pop)
	coeffs = np.power(dist_arr, 2)*(pop)
	coeffs = coeffs.flatten()
	return coeffs

'''
input the number of districts and the size of each district, 
districts = int
pop = list of population sizes for each census block
return = array
'''

def pop_constraint(districts, pop):
	num_districts = len(districts)
	size = (1.0/num_districts)*np.sum(pop)
	arr = size*np.ones(num_districts)
	return arr

'''
input polling locations (list)
input populations of each census block (list)
forms a matrix that enforces populations to sum limit
w1x(1,1) + ... + wkx(1,k) = P
returns an array
'''

def build_pop_constraints(districts, pop):
	pop_len = len(pop)
	num_rows = len(districts)
	num_cols = num_rows*pop_len
	cons_mat = np.zeros((num_rows, num_cols))
	for i in range(num_rows):
		cons_mat[i, i*pop_len:(i+1)*pop_len] = pop[:]
	return cons_mat

'''
input polling locations (list)
input populations of each census block (list)
builds sum constraint matrix for x(i,j) so that they sum to 1
returns array
'''

def build_sum_constraints(districts, pop):
	pop_len = len(pop)
	num_dist = len(districts)
	num_rows = len(pop)
	num_cols = num_dist*pop_len
	cons_mat = np.zeros((num_rows, num_cols))
	for i in range(num_rows):
		cons_mat[i, i:num_cols:pop_len] = 1
	return cons_mat

def build_constraint_matrix(districts, pop):
	A_top = build_pop_constraints(districts, pop)
	A_bot = build_sum_constraints(districts, pop)
	constraints = np.concatenate((A_top, A_bot), axis = 0)
	return constraints



	
'''
read in districts, distances, and pop
'''
if __name__ == "__main__":
	districts = [1, 1]
	pop = [10, 20, 30]
	dist = [[2, 3, 4],[5, 1, 3]]
	coeffs = get_coeffs(dist, pop)
	pop_constrs = pop_constraint(districts, pop)
	ones = np.ones(len(pop))
	eq = np.concatenate((pop_constrs, ones), axis = 0)
	A = build_constraint_matrix(districts, pop)
	print('coeffs: ', coeffs)
	print('equality: ', eq)
	print('constraints: ', A)
	print(optimize.linprog(coeffs, A_eq = A, b_eq = eq, bounds = [0,1]))

	









