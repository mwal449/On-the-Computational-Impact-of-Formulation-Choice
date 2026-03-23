# On-the-Computational-Impact-of-Formulation-Choice
A large scale study of the link between formulation choice and computational performance on the maximum stable set problem.

This repository contains the code and data used in the project.

Code Files:

The `functions.py` file contains:
       The functions used to generate Erdős-Rényi and recursive Markov instances.
       The functions neede to test each formulation on a given instance.

A sample workflow corresponding to the procedure outlined in Chapter 3 of the dissertation is provided in the Jupter notebook `example_function_usage.ipynb`. This notebook also includes examples showing how to produce performance profiles and boxplots for a range of test instances

Erdős-Rényi Data
The results for testing the 16 formulations `E1B1, E1B2, E1B4, E2B1, E2B2, E2B4, E3B1, E3B2, E3B3, E3B4, E1SB1, E1SB2, E1SB4, E3SB1, E3SB2 and E3SB4` on the 1,500 Erdős-Rényi instances used in the project are stored in the file `github_final_ER_results.pkl`

The file does not contain graph matrices, since including them would make the file too large to upload to GitHub. Please contact me if you need these matrices.

The columns of `github_final_ER_results.pkl` are: 

       
       ['N', 'p', 'E1B1_solution_times',
       'E1B1_optimal_values', 'E1B2_solution_times', 'E1B2_optimal_values',
       'E1B4_solution_times', 'E1B4_optimal_values', 'E2B1_solution_times',
       'E2B1_optimal_values', 'E2B2_solution_times', 'E2B2_optimal_values',
       'E2B4_solution_times', 'E2B4_optimal_values', 'E3B1_solution_times',
       'E3B1_optimal_values', 'E3B2_solution_times', 'E3B2_optimal_values',
       'E3B4_solution_times', 'E3B4_optimal_values', 'E1SB1_solution_times',
       'E1SB1_optimal_values', 'E1SB2_solution_times', 'E1SB2_optimal_values',
       'E1SB4_solution_times', 'E1SB4_optimal_values', 'E3SB1_solution_times',
       'E3SB1_optimal_values', 'E3SB2_solution_times', 'E3SB2_optimal_values',
       'E3SB4_solution_times', 'E3SB4_optimal_values', 'E3B3_solution_times',
       'E3B3_optimal_values']

Markov Graph Data:
The data set for testing the 9 formulations `E1B1, E1B2, E1B4, E2B1, E2B2, E2B4, E3B1, E3B2, E3B4` on 1080 Markov Graphs are stored in the file `Markov_graph_data.pkl`

The notebook `generating_markov_plots.ipynb` contains the code used to generate the plots for the Markov graph section of the report. It uses data from `Markov_graph_data.pkl`.

This notebook also shows how to compute the `p_hat` value for each graph from its matrix. However, the `.pkl` file does not contain the matrices because of GitHub upload limitations.


Plots for Erdős-Rény graphs and DIMACS graphs can be generated analogously.
