#!/usr/bin/env python3

from itertools import permutations
from time import time

def new_graph(file):
    ''' 
    This function processes the input data, which is formatted as follows: 
    * Multiple test cases in the file
    * First line of each case starts with a c followed by:
        - a test case number
        - an h for hamiltonian (or n for not)
    * 2nd line  starts with a p
        - followed by a u (undirected) or d (directed)
        - followed by the number of variables
        - followed by the number of edges
    * following lines are of two types
        - starts with a v, followed by a list of the names of the vertices
        - starts with an e, followed by the source vertex, followed by the target vertex (note for undirected graphs there is an edge going the other way)
    '''
    # Find if graph is directed or undirected and the number of edges
    _, d, _, e = file.readline().strip().split(',')
    directed = True if d == 'd' else False
    # Add vertices to list
    verts = file.readline().strip().split(',')[1:]
    edges = []
    # Add edges to list
    for _ in range(int(e)):
        v1, v2 = file.readline().strip().split(',')[1:]
        if not directed: # if undirected, add edge going both ways
            edges.append((v1, v2))
            edges.append((v2, v1))
        else:
            edges.append((v1, v2))

    return verts, edges

def find_hamiltonian(verts, edges):
    # Compute start time
    start_time = time()
    if len(verts) == 1: # if there is only one vertex, it is automatically hamiltonian, so return True
        end_time = time()
        return True, end_time - start_time
    # To determine if a graph has a hamiltonian path, I used brute force:
    #   * Compute every possible permutation of vertice orders
    #   * Make sure there is a path between each consecutive vertex in path
    #   * If there is not an edge between two consecutive vertices, skip to next permutation
    #   * If it gets to the end of the permutation with valid paths, compute end time and return True
    #   * If we break out of the for loop, that means that we went through every permutation and found no Hamiltonian path: return False
    for path in permutations(verts):
        for i in range(len(verts)-1):
            if (path[i], path[i+1]) not in edges:
                break
            if i == len(verts) - 2:
                end_time = time()
                return True, end_time - start_time
    
    end_time = time()
    return False, end_time - start_time

def main():
    # Open the data file to read from and create the output file to write to
    with open("data_ekoran.csv", mode='r') as input_file:
        with open("output_ekoran.csv", mode='w') as output_file: 
            output_file.write("Case_Number,nVertices,Is_Hamiltonian,Elapsed_Time\n")
            for line in input_file:
                parameters = line.strip().split(',') # Find the start each graph
                if parameters[0] == 'c':
                    case = parameters[1] # Graph test case number
                    hamiltonian = True if parameters[2] == 'h' else False # To verify the output of the function 
                    vertices, edges = new_graph(input_file) # Process Graph input
                # Find hamiltonian path and write results in output file
                result, elapsed_time = find_hamiltonian(vertices, edges) 
                output_file.write(f'{case},{len(vertices)},{result},{elapsed_time}\n')
                # Print results to stdout
                print(f'Graph {case}:')
                print(f'  Number of Vertices: {len(vertices)}')
                print(f'  Number of Edges: {len(edges)}')
                print(f'  Hamiltonian Result: {result}')
                print(f'  Expected Result: {hamiltonian}')
                print(f'  Elapsed Time: {elapsed_time}')


if __name__ == "__main__":
    main()