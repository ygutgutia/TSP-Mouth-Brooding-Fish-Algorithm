# encoding:utf-8
from operator import attrgetter
import random, sys, time, copy, math, operator, time

# class that represents a graph
class Graph:

	def __init__(self, number_vertices):
		self.edges = {} # dictionary of edges
		self.vertices = set() # set of vertices
		self.number_vertices = number_vertices # amount of vertices

	# adds a edge linking "src" in "dest" with a "cost"
	def addEdge(self, src, dest, cost = 0):
		# checks if the edge already exists
		if not self.existsEdge(src, dest):
			self.edges[(src, dest)] = cost
			self.vertices.add(src)
			self.vertices.add(dest)

	# checks if exists a edge linking "src" in "dest"
	def existsEdge(self, src, dest):
		return (True if (src, dest) in self.edges else False)

	# shows all the links of the graph
	def showGraph(self):
		print('Showing the graph:\n')
		for edge in self.edges:
			print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

	# returns total cost of the path
	def getCostPath(self, path):
		total_cost = 0
		for i in range(self.number_vertices - 1):
			total_cost += self.edges[(path[i], path[i+1])]
		# add cost of the last edge
		total_cost += self.edges[(path[self.number_vertices - 1], path[0])]
		return total_cost

	# gets random unique paths - returns a list of lists of paths
	def getRandomPaths(self, max_size):
		random_paths, list_vertices = [], list(self.vertices)
		initial_vertice = random.choice(list_vertices)
		if initial_vertice not in list_vertices:
			print('Error: initial vertice %d not exists!' % initial_vertice)
			sys.exit(1)
		list_vertices.remove(initial_vertice)
		list_vertices.insert(0, initial_vertice)
		for i in range(max_size):
			list_temp = list_vertices[1:]
			random.shuffle(list_temp)
			list_temp.insert(0, initial_vertice)
			if list_temp not in random_paths:
				random_paths.append(list_temp)
		return random_paths


# class that represents a complete graph
class CompleteGraph(Graph):
	# generates a complete graph
	def generates(self):
		for i in range(self.number_vertices):
			for j in range(self.number_vertices):
				if i != j:
					weight = random.randint(1, 10)
					self.addEdge(i, j, weight)


# class that represents a chromosome
class Chromosome:

	def __init__(self, solution, cost):
		# current solution
		self.solution = solution
		# best solution (fitness) it has achieved so far
		self.pbest = solution
		# set costs of current soln and personal best soln
		self.cost_current_solution = cost
		self.cost_pbest_solution = cost
		# velocity of a chromosome is a sequence of 3-tuple
		# (1, 2, 'beta') means SO(1,2), with a probability of "beta"
		self.velocity = []

	# set pbest
	def setPBest(self, new_pbest):
		self.pbest = new_pbest

	# returns the pbest
	def getPBest(self):
		return self.pbest

	# set the new velocity (sequence of swap operators)
	def setVelocity(self, new_velocity):
		self.velocity = new_velocity

	# returns the velocity (sequence of swap operators)
	def getVelocity(self):
		return self.velocity

	# set solution
	def setCurrentSolution(self, solution):
		self.solution = solution

	# gets solution
	def getCurrentSolution(self):
		return self.solution

	# set cost pbest solution
	def setCostPBest(self, cost):
		self.cost_pbest_solution = cost

	# gets cost pbest solution
	def getCostPBest(self):
		return self.cost_pbest_solution

	# set cost current solution
	def setCostCurrentSolution(self, cost):
		self.cost_current_solution = cost

	# gets cost current solution
	def getCostCurrentSolution(self):
		return self.cost_current_solution

	# removes all elements of the list velocity
	def clearVelocity(self):
		del self.velocity[:]


# MBF algorithm
class MBF:

	def __init__(self, graph, iterations, nFish, alpha = 1, beta = 1, sp = 1, spdamp = 1, crossover_count = 0.65):
		self.graph = graph # the graph
		self.iterations = iterations # max of iterations
		self.nFish = nFish # fish size population
		self.chromosomes = [] # list of chromosomes
		self.alpha = alpha # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.beta = beta # the probability that all swap operators in swap sequence (pbest - x(t-1))
		self.sp = sp # the probability that all swap operators in v(t-1)
		self.spdamp = spdamp # damping constant
		self.crossover_count = crossover_count # percentage of crossover from fitter parent

		# initialized with a group of random chromosomes (solutions)
		solutions = self.graph.getRandomPaths(self.nFish)
		# checks if exists any solution
		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)
		# creates the chromosomes and initialization of swap sequences in all the chromosomes
		for solution in solutions:
			# creates a new chromosome
			chromosome = Chromosome(solution=solution, cost=graph.getCostPath(solution))
			# add the chromosome
			self.chromosomes.append(chromosome)
		# updates "Fish Population"
		self.nFish = len(self.chromosomes)

	# set gbest (best chromosome of the population)
	def setGBest(self, new_gbest):
		self.gbest = new_gbest

	# returns gbest (best chromosome of the population)
	def getGBest(self):
		return self.gbest

	# shows the info of the chromosomes
	def showsChromosomes(self):
		print('Showing chromosomes...\n')
		for chromosome in self.chromosomes:
			print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent solution: %s\t|\tcost current solution: %d' \
				% (str(chromosome.getPBest()), chromosome.getCostPBest(), str(chromosome.getCurrentSolution()), chromosome.getCostCurrentSolution()))
		print('')
 

	# the mbf algorithm
	def run(self):
		# for each time step (iteration)
		for t in range(self.iterations):
			# updates gbest (best chromosome of the population)
			self.gbest = min(self.chromosomes, key = attrgetter('cost_pbest_solution'))
			# for each chromosome in the population
			for chromosome in self.chromosomes:
				chromosome.clearVelocity()
				temp_velocity = []
				prev_velocity = chromosome.getVelocity()[:] #Fetches v(t-1)
				solution_gbest = copy.copy(self.gbest.getPBest()) # gets solution of the gbest
				solution_pbest = chromosome.getPBest()[:] # copy of the pbest solution
				solution_chromosome = chromosome.getCurrentSolution()[:] # gets copy of the current solution of the chromosome
			
				# generates all swap operators to calculate v(t-1)
				# generates swap operator
				for swap_operator in prev_velocity:
					if random.random() <= swap_operator[2]:
						swap_operator[2] = self.sp #Probability of sp
					else:
						swap_operator[2] = 0 #Else probability of 0
					# append swap operator in the list of velocity
					temp_velocity.append(swap_operator)


				# generates all swap operators to calculate (pbest - x(t-1))
				for i in range(self.graph.number_vertices):
					if solution_chromosome[i] != solution_pbest[i]:
						# generates swap operator
						swap_operator = (i, solution_pbest.index(solution_chromosome[i]), self.alpha)
						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)
						# makes the swap
						aux = solution_pbest[swap_operator[0]]
						solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
						solution_pbest[swap_operator[1]] = aux


				# generates all swap operators to calculate (gbest - x(t-1))
				for i in range(self.graph.number_vertices):
					if solution_chromosome[i] != solution_gbest[i]:
						# generates swap operator
						swap_operator = (i, solution_gbest.index(solution_chromosome[i]), self.beta)
						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)
						# makes the swap
						aux = solution_gbest[swap_operator[0]]
						solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
						solution_gbest[swap_operator[1]] = aux


				# generates new solution for chromosome
				for swap_operator in temp_velocity:
					if random.random() <= swap_operator[2]:
						# makes the swap
						aux = solution_chromosome[swap_operator[0]]
						solution_chromosome[swap_operator[0]] = solution_chromosome[swap_operator[1]]
						solution_chromosome[swap_operator[1]] = aux
				

				# updates velocity
				chromosome.setVelocity(temp_velocity)
				# updates the current solution
				chromosome.setCurrentSolution(solution_chromosome)
				# gets cost of the current solution
				cost_current_solution = self.graph.getCostPath(solution_chromosome)
				# updates the cost of the current solution
				chromosome.setCostCurrentSolution(cost_current_solution)
				# checks if current solution is pbest solution
				if cost_current_solution < chromosome.getCostPBest():
					chromosome.setPBest(solution_chromosome)
					chromosome.setCostPBest(cost_current_solution)

			
			#Updating Source Power due to damping
			self.sp = self.sp * self.spdamp
			#Single Point Crossover
			#Select first and second partner
			first_parent = random.choice(self.chromosomes)
			first_parent_solution = first_parent.getCurrentSolution()
			second_parent = random.choice([x for x in self.chromosomes if x != first_parent])
			second_parent_solution = second_parent.getCurrentSolution()
			#First parent is more fit
			if first_parent.getCostCurrentSolution() > second_parent.getCostCurrentSolution():
				temp = second_parent
				second_parent = first_parent
				first_parent = temp
			
			#Crossover point is 65% of better parent (1st child)
			crossover_point = (int)(self.graph.number_vertices * self.crossover_count)
			child1_solution = [None] * self.graph.number_vertices
			for i in range(0, crossover_point):
				child1_solution[i] = first_parent_solution[i]
			pointer = 0
			for i in range(crossover_point, self.graph.number_vertices):
				while second_parent_solution[pointer] in child1_solution:
					pointer += 1
				child1_solution[i] = second_parent_solution[pointer]
 
			#Crossover point is 65% of better parent (2nd child)
			crossover_point = (int)(self.graph.number_vertices * (1 - self.crossover_count))
			child2_solution = [None] * self.graph.number_vertices
			for i in range(crossover_point, self.graph.number_vertices):
				child2_solution[i] = first_parent_solution[i]
			pointer = 0
			for i in range(0, crossover_point):
				while second_parent_solution[pointer] in child2_solution:
					pointer += 1
				child2_solution[i] = second_parent_solution[pointer]
 
			first_parent.setVelocity([])
			first_parent.setCurrentSolution(child1_solution)
			cost_current_solution = self.graph.getCostPath(child1_solution)
			first_parent.setCostCurrentSolution(cost_current_solution)
			if cost_current_solution < first_parent.getCostPBest():
				first_parent.setPBest(child1_solution)
				first_parent.setCostPBest(cost_current_solution)
  
			second_parent.setVelocity([])
			second_parent.setCurrentSolution(child2_solution)
			cost_current_solution = self.graph.getCostPath(child2_solution)
			second_parent.setCostCurrentSolution(cost_current_solution)
			if cost_current_solution <second_parent.getCostPBest():
				second_parent.setPBest(child2_solution)
				second_parent.setCostPBest(cost_current_solution)

# main function
if __name__ == "__main__":

	start = time.time()    
	print("Enter the number of vertices\n")
	n = (int)(input())
 
	# random graph
	print('Random graph...')
	random_graph = CompleteGraph(number_vertices = n)
	random_graph.generates()
	#random_graph.showGraph() # If you wish to view the graph
 
	# sp - (0, 1), spdamp - (0.85, 0.95), alpha - Generally 1, Beta - (0, 1), crossover count - 65%
	mbf = MBF(random_graph, iterations = 10000, nFish = 20, alpha = 1, beta = 0.9, sp = 0.5, spdamp = 0.85, crossover_count = 0.65)
	mbf.run()
	print('gbest: %s | cost: %d\n' % (mbf.getGBest().getPBest(), mbf.getGBest().getCostPBest()))
	end = time.time()
	print("Time taken ", end - start)
 
	# use for Text type input
''' 
	start = time.time()    
	graph = Graph(number_vertices = n)
	with open('./input.txt') as f:
		for line in f.readlines():
			city = line.split(' ')
			graph.addEdge(int(city[0]), int(city[1]), int(city[2]))

	# creates a MBF instance
	# sp - (0, 1), spdamp - (0.85, 0.95), alpha - Generally 1, Beta - (0, 1), crossover count - 65%
	mbf = MBF(graph, iterations = 100, nFish = 10, alpha = 1, beta = 0.9, sp = 0.5, spdamp = 0.85, crossover_count = 0.65)
	mbf.run() # runs the MBF algorithm
	mbf.showsChromosomes() # shows the chromosomes
	# shows the global best chromosome
	print('gbest: %s | cost: %d\n' % (mbf.getGBest().getPBest(), mbf.getGBest().getCostPBest()))
	end = time.time()
	print("Time taken ", end - start)

'''