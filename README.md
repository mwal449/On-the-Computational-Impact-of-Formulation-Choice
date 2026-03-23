# On-the-Computational-Impact-of-Formulation-Choice
A large scale study of the link between formulation choice and computational performance on the maximum stable set problem.

The functions used to generate Erdős-Rényi and Recursive Markov Instances are contained in the file functions.py

The functions.py file also contains the necessary functions to test each formulation on a given instance. A sample of the workflow outlined in Chapter 3 is provided in the jupyter notebook example_function_usage.ipynb
       Examples of how to plot performance profiles and box plots for a range of test instances are also shown in this Jupyter Notebook.
       


       
The data set for testing the 15 formulations E1B1, E1B2, E1B4, E2B1, E2B2, E2B4, E3B1, E3B2, E3B4, E1SB1, E1SB2, E1SB4, E3SB1, E3SB2 and E3SB4 on the 1,500 Erdős-Rényi instances we tested in the project are contained in the pkl file github_final_ER_results.pkl
       This file does not have graph matrices as the file is too large to upload to github if they are included. Please contact me for these if necessary.
       The columns of this file are as follows:
       
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

The data set for testing the 9 formulations E1B1, E1B2, E1B4, E2B1, E2B2, E2B4, E3B1, E3B2, E3B4 on 1080 Markov Graphs is included in the pkl file..,

The data set for testing the 9 formulations E1B1, E1B2, E1B4, E2B1, E2B2, E2B4, E3B1, E3B2, E3B4 on the 24 DIMACS instances is included in the pkl file...

We present the code we used to generate the plots for the Markov section of this report in the file...
  The plots for Erdős-Renyi graphs and DIMACS graphs can be generated analogously

