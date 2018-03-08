# File: GeneticOperation
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/23/18

import NodeController as nc
import InputNode as inode 
import HiddenNode as hnode
import OutputNode as onode
import Connection as con
import numpy as np



def init_env(in_num, out_num, state, cont):
	'''Initialize the input and output
	nodes to a specified state'''
	for i in range(in_num):
		node = inode.InputNode("input_node_" + str(i))
		node.state = state
		cont.add_node(node)
	for i in range(out_num):
		node = onode.OutputNode("output_node_" + str(i))
		cont.add_node(node)

def add_hidden(cont, ntype="Input"):
	'''adds a hidden node in a random
	location. Based on the ntype flag
	it will be input or output'''
	num = len(cont.hiddens)
	n = hnode.HiddenNode("hidden_node_" + str(num), cont)
	cont.add_node(n)
	if ntype == "Input":
		r = np.random.randint(0,  len(cont.inputs))
		add = cont.get_node("input_node_" + str(r))
		c = con.Connection(add, n, cont)
	else:	
		r =  np.random.randint(0,  len(cont.outputs))
		cont.get_count()
		add = cont.get_node("output_node_" + str(r))
		c = con.Connection(n, add, cont)
	

def print_current(cont):
	'''Print the topology 
	of the current species'''
	print("Input Nodes:")
	for i in cont.inputs:
		print(cont.get_node(i))
	print("Hidden Nodes:")
	for i in cont.hiddens:
		print(cont.get_node(i))
	print("Outpus Nodes:")
	for i in cont.outputs:
		print(cont.get_node(i))

def get_fitness(cont, func):
	'''function decorator to 
	be decided by the implementer'''
	return func(cont)

def reg_fitness(cont):
	'''Returns a dummy fitness score 
	for testing'''
	return np.random.randint(50000) # [0,50000)

def reg_input(cont):
	'''returns a dummy input for
	testing'''
	return np.random.randint(2) # [0,2)

# Algorithm is as follows:
#	initialize population
#	evaluate fitness of initial population
#	while (iterations less than fixed value):
#		make children
#		mutate children
#		evaluate fitness
#	end while
#
def NEAT(iterations, 				# The number of times the algorithm runs 
		init_pop, 	 				# The initial populations size
		fitness_func=reg_fitness,	# The fitness function to be used
		input_func=reg_input, 		# The input function that sets the states of input nodes
		input_count=10,				# The number of input nodes
		output_count=10):			# The number of output nodes
	species = []					# tuples with reference to Controller and fitness score
	avg_fitness = 0	

	tally = 0				
	for i in range(init_pop):		# initialize population
		cont = nc.NodeController()
		init_env(input_count, output_count, 0, cont)
		add_hidden(cont, ntype="Output")
		species.append((cont, get_fitness(cont, fitness_func))) # evaluate fitness of init pop
		tally += species[i][1]
	avg_fitness = tally / init_pop 	# just the mean
	sorted(species, key=lambda x: x[1]) # sort by the fitnesss score


	for j in range(iterations):
		print_current(species[0][0])
		for i in range(init_pop):
			species[i][0].process_inputs(input_func)
			for k in range(len(species[i][0].hiddens)): # get the input and process it
				species[i][0].get_node(species[i][0].hiddens[k]).process()


		next_species = []			# make children
		for i in range(init_pop):
			if species[i][1] > avg_fitness: # reproduce the systems that are better only
				cont = species[i][0].copy()
				if np.random.randint(2) == 1: # flip a coin whether input or output
					add_hidden(cont, ntype="Input")
				else:
					add_hidden(cont, ntype="Output")
			else:
				cont = nc.NodeController()
				init_env(input_count, output_count, 0, cont)
				if np.random.randint(2) == 1: # flip a coin whether input or output
					add_hidden(cont, ntype="Input")
				else:
					add_hidden(cont, ntype="Output")
			next_species.append((cont, get_fitness(cont, fitness_func))) #evaluate fitness
		species.clear()
		species = next_species.copy()
		sorted(species, key=lambda x: x[1]) # sort by the fitnesss score
	print_current(species[0][0])

