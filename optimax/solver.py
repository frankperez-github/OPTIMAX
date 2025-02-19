import numpy as np
from scipy.optimize import linprog
import pulp
from optimax.parser import ProblemInstance
from optimax.utils import validate_dimensions
from optimax.visualizer import Visualizer  # Assuming Visualizer is imported for plotting

class Solver:
    @staticmethod
    def solve_lp(problem: ProblemInstance, method: str = 'highs') -> dict:
        """
        Solves a linear programming problem using scipy.optimize.linprog.

        Parameters:
            problem (ProblemInstance): The problem instance.
            method (str): The solver method. Use 'highs' for simplex and 'highs-ds' for dual simplex.

        Returns:
            dict: A dictionary containing the solution status, optimal value, and variable assignments.
        """
        # Adjust objective coefficients for minimization (linprog minimizes by default)
        c = problem.function_objective[:]
        if problem.objective == "maximizar":
            c = [-coef for coef in c]
        
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        
        for cons in problem.constraints:
            coefs = cons["coeficientes"]
            sign = cons["signo"]
            rhs = cons["valor"]
            if sign == "<=":
                A_ub.append(coefs)
                b_ub.append(rhs)
            elif sign == ">=":
                # Convert to <= by multiplying both sides by -1
                A_ub.append([-x for x in coefs])
                b_ub.append(-rhs)
            elif sign == "==":
                A_eq.append(coefs)
                b_eq.append(rhs)
            else:
                raise ValueError(f"Unsupported constraint sign: {sign}")
        
        bounds = [(0, None) for _ in problem.function_objective]
        
        # Track iterations and objective values for convergence plot
        iterations = []
        objective_values = []
        
        def callback(res):
            """
            Callback function to track iterations and objective function values.
            """
            iterations.append(len(iterations) + 1)
            if res.x is not None: 
                objective_values.append(np.dot(c, res.x))

        result = linprog(
            c=c,
            A_ub=A_ub if A_ub else None,
            b_ub=b_ub if b_ub else None,
            A_eq=A_eq if A_eq else None,
            b_eq=b_eq if b_eq else None,
            bounds=bounds,
            method=method,
            #callback=callback
        )

        
        if result.success:
            optimal_value = result.fun if problem.objective == "minimizar" else -result.fun
            Visualizer.plot_convergence(iterations, objective_values)
            return {
                "status": result.message,
                "optimal_value": optimal_value,
                "variables": result.x.tolist(),
                "iterations": iterations,
                "objective_values": objective_values
            }
        else:
            return {"status": result.message}
    
    @staticmethod
    def solve_ilp(problem: ProblemInstance) -> dict:
        """
        Solves an Integer Linear Programming (ILP) problem using PuLP, which employs Branch & Bound.

        Parameters:
            problem (ProblemInstance): The problem instance.

        Returns:
            dict: A dictionary containing the solution status, optimal value, and variable assignments.
        """
        sense = pulp.LpMaximize if problem.objective == "maximizar" else pulp.LpMinimize
        prob = pulp.LpProblem("ILP_Problem", sense)
        
        variables = []
        for i, is_int in enumerate(problem.variables_integer):
            if is_int:
                var = pulp.LpVariable(f"x_{i}", lowBound=0, cat=pulp.LpInteger)
            else:
                var = pulp.LpVariable(f"x_{i}", lowBound=0, cat=pulp.LpContinuous)
            variables.append(var)
        
        prob += pulp.lpSum([coef * var for coef, var in zip(problem.function_objective, variables)])
        
        for cons in problem.constraints:
            coefs = cons["coeficientes"]
            sign = cons["signo"]
            rhs = cons["valor"]
            expr = pulp.lpSum([coef * var for coef, var in zip(coefs, variables)])
            if sign == "<=":
                prob += (expr <= rhs)
            elif sign == ">=":
                prob += (expr >= rhs)
            elif sign == "==":
                prob += (expr == rhs)
            else:
                raise ValueError(f"Unsupported constraint sign: {sign}")
        
        result_status = prob.solve()
        
        branch_tree_data = []
        
        if pulp.LpStatus[result_status] == "Optimal":
            optimal_value = pulp.value(prob.objective)
            return {
                "status": pulp.LpStatus[result_status],
                "optimal_value": optimal_value,
                "variables": [pulp.value(v) for v in variables],
                "branch_tree_data": branch_tree_data
            }
        else:
            return {"status": pulp.LpStatus[result_status]}
    
    @classmethod
    def solve(cls, problem: ProblemInstance, algorithm: str) -> dict:
        """
        Main method to solve a problem instance using the selected algorithm.

        Parameters:
            problem (ProblemInstance): The problem instance.
            algorithm (str): One of 'simplex', 'dual_simplex', or 'branch_and_bound'.

        Returns:
            dict: The solution as returned by the appropriate solver.
        """
        if validate_dimensions(problem):
            if algorithm in ["simplex", "dual_simplex"]:
                method = "highs" if algorithm == "simplex" else "highs-ds"
                return cls.solve_lp(problem, method=method)
            elif algorithm == "branch_and_bound":
                return cls.solve_ilp(problem)
            else:
                raise ValueError(f"Unsupported algorithm type: {algorithm}")
        else:
            print("Check the dimensions of your problem again.")
