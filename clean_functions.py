import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import random
import networkx as nx
import gurobipy as gp
from gurobipy import Model, GRB, quicksum
import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt






def gen_graph_mat(n, p):
    """Generate the adjacency matrix of an undirected random graph using the Erdős–Rényi model G(n, p).

    Parameters:
    n : int
        Number of vertices in the graph.
    p : float
        Probability that any given edge is included. Should lie in [0, 1].

    Output:
    numpy.ndarray
        An `n x n` adjacency matrix with entries ij 1 when an edge exists between the i-th
          and j-th vertices, and 0 otherwise."""
        

    graph_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                graph_matrix[i][j] = 1
                graph_matrix[j][i] = 1
    return graph_matrix







def matrix_to_list(matrix):
    """Convert an adjacency matrix to a list of edges.

    Parameters:
    matrix : numpy.ndarray
        An `n x n` adjacency matrix with entries ij 1 when an edge exists between the i-th
          and j-th vertices, and 0 otherwise

    Returns:
    list of lists
        A list of edges, where each edge is represented as a list [i, j] with i < j."""

    n = len(matrix)
    return [[i,j] for i in range(n) for j in range(i+1,n) if matrix[i][j] == 1]








def model_building_function(model, n, edges_list):
    """Build a Gurobi model for the Maximum Stable Set problem based on the specified formulation and graph
    
    Parameters:
    model : str
        A string indicating the formulation type (e.g., "E1B1", "E1B2", etc.)
    n : int
        Number of vertices in the graph
    edges_list : list of lists
        A list of containing the edges in the specified graph, where each edge is represented as a list [i, j] with i < j
    
    Returns:
    model_instance : gurobipy.Model
        The constructed Gurobi model instance for the specified formulation and graph  
    """





    if model == "E1B1":
        model_instance = gp.Model("MSS_Binary")
        x = [model_instance.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]* x[j] == 0 , name=f"edge_{i}_{j}")

        # Create the objective functionßss
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E1B2":
        model_instance = gp.Model("MSS_Anjos_1")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 = x for each x[i]
        for i in range(n):
            model_instance.addConstr(x[i]**2 -x[i] == 0 , name=f"binary_{i}")


        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] == 0 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E1B3":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Add the binary constraint using formulation B3 for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(0 <= x[i], name=f"lower_{i}")
            model_instance.addConstr(x[i] <= 1, name=f"upper_{i}")
            model_instance.addConstr(x[i]*x[i] - x[i] >= 0, name=f"binary_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] == 0 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x

    
    if model == "E1B4":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        y = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}") for i in range(n)]

        model_instance.params.NonConvex = 2

        # Add the corresponding binary constraints (auxillary variables yi)
        for i in range(n):
            model_instance.addConstr(x[i] + y[i] == 1, name=f"binary_{i}")
            model_instance.addConstr(x[i]* y[i] == 0, name=f"prod_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] == 0 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    

##################### E2 ############################



    if model == "E2B1":
        model_instance = gp.Model("MSS_Linear_Binary")
        x = [model_instance.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]+x[j] <= 1 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    
    
    if model == "E2B2":
        model_instance = gp.Model("MSS_Anjos_3")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 = x for each x[i]
        for i in range(n):
            model_instance.addConstr(x[i]**2 -x[i] == 0 , name=f"binary_{i}")


        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]+x[j] <= 1 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x


    if model == "E2B3":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 - x >= 0 for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(0 <= x[i], name=f"lower_{i}")
            model_instance.addConstr(x[i] <= 1, name=f"upper_{i}")
            model_instance.addConstr(x[i]*x[i] - x[i] >= 0, name=f"binary_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]+x[j] <=1 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    

    if model == "E2B4":
        model_instance = gp.Model("MSS_Quadratic_3")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        y = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(x[i] + y[i] == 1, name=f"binary_{i}")
            model_instance.addConstr(x[i]* y[i] == 0, name=f"prod_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]+x[j] <= 1 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x




##################### E3 ############################

    

    if model == "E3B1":
        model_instance = gp.Model("MSS_Linear_Binary_3")
        x = [model_instance.addVar(vtype= GRB.BINARY, name = f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] <= 0 , name=f"edge_{i}_{j}")


        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    

    if model == "E3B2":
        model_instance = gp.Model("MSS_Anjos_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 = x for each x[i]
        for i in range(n):
            model_instance.addConstr(x[i]**2 -x[i] == 0 , name=f"binary_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] <= 0 , name=f"edge_{i}_{j}")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    
    
    if model == "E3B3":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Add the binary constraint using formulation B3 for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(0 <= x[i], name=f"lower_{i}")
            model_instance.addConstr(x[i] <= 1, name=f"upper_{i}")
            model_instance.addConstr(x[i]*x[i] - x[i] >= 0, name=f"binary_{i}")

        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] <= 0 , name=f"edge_{i}_{j}")
        
        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E3B4":        
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        y = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the corresponding binary constraints (auxillary variables yi)
        for i in range(n):
            model_instance.addConstr(x[i] + y[i] == 1, name=f"binary_{i}")
            model_instance.addConstr(x[i]* y[i] == 0, name=f"prod_{i}")

        
        # Add the edge constraints
        for edge in edges_list:
            i = edge[0]
            j = edge[1]
            model_instance.addConstr(x[i]*x[j] <= 0 , name=f"edge_{i}_{j}")
        
        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    



    ##                      Sum Edges Formulation   ##

    #E1S Formulations

    if model == "E1SB1":
        model_instance = gp.Model("MSS_Binary")
        x = [model_instance.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(
            gp.quicksum(x[i] * x[j] for i, j in edges_list) == 0,name="all_edges_sum")
        

        # Create the objective functionßss
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E1SB2":
        model_instance = gp.Model("MSS_Anjos_1")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 = x for each x[i]
        for i in range(n):
            model_instance.addConstr(x[i]**2 -x[i] == 0 , name=f"binary_{i}")


        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) == 0, name="all_edges_sum")


        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E1SB3":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Add the binary constraint using formulation B3 for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(0 <= x[i], name=f"lower_{i}")
            model_instance.addConstr(x[i] <= 1, name=f"upper_{i}")
            model_instance.addConstr(x[i]*x[i] - x[i] >= 0, name=f"binary_{i}")

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) == 0, name="all_edges_sum")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x

    
    if model == "E1SB4":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        y = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}") for i in range(n)]

        model_instance.params.NonConvex = 2

        # Add the corresponding binary constraints (auxillary variables yi)
        for i in range(n):
            model_instance.addConstr(x[i] + y[i] == 1, name=f"binary_{i}")
            model_instance.addConstr(x[i]* y[i] == 0, name=f"prod_{i}")

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) == 0, name="all_edges_sum")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x


    ##                      E3S Formulations            ##


    if model == "E3SB1":
        model_instance = gp.Model("MSS_Linear_Binary_3")
        x = [model_instance.addVar(vtype= GRB.BINARY, name = f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) <= 0, name="all_edges_sum")


        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    

    if model == "E3SB2":
        model_instance = gp.Model("MSS_Anjos_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the binary constraint using formulation x^2 = x for each x[i]
        for i in range(n):
            model_instance.addConstr(x[i]**2 -x[i] == 0 , name=f"binary_{i}")

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) <= 0, name="all_edges_sum")

        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    
    
    if model == "E3SB3":
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2


        # Add the binary constraint using formulation B3 for each x[i] (x in [0,1])
        for i in range(n):
            model_instance.addConstr(0 <= x[i], name=f"lower_{i}")
            model_instance.addConstr(x[i] <= 1, name=f"upper_{i}")
            model_instance.addConstr(x[i]*x[i] - x[i] >= 0, name=f"binary_{i}")

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) <= 0, name="all_edges_sum")
        
        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x
    


    if model == "E3SB4":        
        model_instance = gp.Model("MSS_Quadratic_2")
        x = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}") for i in range(n)]
        y = [model_instance.addVar(vtype=GRB.CONTINUOUS, name=f"y_{i}") for i in range(n)]
        model_instance.params.NonConvex = 2

        # Add the corresponding binary constraints (auxillary variables yi)
        for i in range(n):
            model_instance.addConstr(x[i] + y[i] == 1, name=f"binary_{i}")
            model_instance.addConstr(x[i]* y[i] == 0, name=f"prod_{i}")

        # Single constraint summing all x_i * x_j over edges
        model_instance.addConstr(gp.quicksum(x[i] * x[j] for i, j in edges_list) <= 0, name="all_edges_sum")
        
        # Create the objective function
        total_nodes = quicksum(x[i] for i in range(n))
        model_instance.setObjective(total_nodes, GRB.MAXIMIZE)

        return model_instance, x





def solve_problem(type, matrix):
    """Solve the Maximum Stable Set problem for a given graph and formulation type, and return the solution time and optimal value.
    
    Parameters:
    type : str
        A string indicating the formulation type (e.g., "E1B1", "E1B2", etc.)

    matrix : numpy.ndarray
        An `n x n` adjacency matrix with entries ij 1 when an edge exists between the i-th
          and j-th vertices, and 0 otherwise corresponding to the graph for which the problem is being solved.

    Returns:
    solution_time : float
        The time taken by the solver to find the optimal solution, measured in seconds.
    optimal_value : float
        The optimal value of the objective function (the size of the maximum stable set) found by the solver."""
    
    
    n = len(matrix)
    edges_list = matrix_to_list(matrix)
    p = 0

    model, x = model_building_function(type, n, p, edges_list)

    start_time = time.time()
    model.optimize()
    end_time = time.time()
    solution_time = end_time - start_time

    optimal_value = model.ObjVal

    return solution_time, optimal_value






def time_limit_solve_problem(type, matrix, time_limit):
    """Solve the Maximum Stable Set problem for a given graph and formulation type with a specified time limit, and return the solution time and found value.

    Parameters:
    type : str
        A string indicating the formulation type (e.g., "E1B1", "E1B2", etc.)
    matrix : numpy.ndarray
        An `n x n` adjacency matrix with entries ij 1 when an edge exists between the i-th
          and j-th vertices, and 0 otherwise corresponding to the graph for which the problem is being solved.
    time_limit : float
        The maximum time (in seconds) allowed for the solver to find a solution. 
         If the solver exceeds this time limit, it will terminate and return the best found solution or bound.

    Returns:
    solution_time : float
        The time taken by the solver to find a solution or reach the time limit, measured in seconds.
           If the time limit is reached without finding an optimal solution, this will be the time until termination.
    """

    n = len(matrix)
    edges_list = matrix_to_list(matrix)
    p = 0

    model, x = model_building_function(type, n, p, edges_list)
    model.setParam('TimeLimit', time_limit)

    start_time = time.time()
    model.optimize()
    end_time = time.time()
    solution_time = end_time - start_time

    # Check solver status
    status = model.Status
    # 9 = time limit reached in Gurobi
    if status == 9:  
        found_value = model.ObjBound  # lower bound
        solution_time = float('nan')  # no true optimal time
    else:
        found_value = model.ObjVal

    return solution_time, found_value


