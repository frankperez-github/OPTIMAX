import sys
from optimax.parser import ProblemInstance
from optimax.selector import AlgorithmSelector
from optimax.solver import Solver
from optimax.visualizer import Visualizer
from optimax.utils import format_solution

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    
    # Read the JSON input file
    try:
        with open(json_file_path, 'r') as f:
            json_input = f.read()
    except Exception as e:
        print("Error reading file:", e)
        sys.exit(1)
    
    # Parse the problem instance from JSON
    try:
        problem = ProblemInstance.from_json(json_input)
    except Exception as e:
        print("Error parsing JSON input:", e)
        sys.exit(1)
    
    # Determine the best algorithm to use based on the problem
    algorithm = AlgorithmSelector.select_algorithm(problem)
    print(f"Selected algorithm: {algorithm}")
    
    # Solve the problem using the selected algorithm
    solution = Solver.solve(problem, algorithm)
    result_status = solution.get("status")
    iterations = solution.get("iterations", None)
    objective_values = solution.get("objective_values", None)
    
    # Output the formatted solution
    print(format_solution(solution))
    
    # Visualize if problem is 2D and has variables
    if len(problem.function_objective) == 2 and "variables" in solution:
        Visualizer.plot_feasible_region(problem, solution)
    
    # Plot convergence if iterations and objective values are available
    if iterations and objective_values:
        Visualizer.plot_convergence(iterations, objective_values)

if __name__ == "__main__":
    main()
