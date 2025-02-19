import numpy as np
from optimax.parser import ProblemInstance

class AlgorithmSelector:
    @staticmethod
    def is_zero_vector_feasible(problem: ProblemInstance) -> bool:
        """
        Checks if the zero vector is a feasible solution for the given problem.
        This is a heuristic to decide if a basic feasible solution exists.
        
        Parameters:
            problem (ProblemInstance): The optimization problem instance.
            
        Returns:
            bool: True if the zero vector satisfies all constraints, False otherwise.
        """
        # Create a zero vector of the appropriate dimension
        x0 = np.zeros(len(problem.function_objective))
        
        # Check each constraint
        for constraint in problem.constraints:
            coefficients = np.array(constraint["coeficientes"])
            sign = constraint["signo"]
            rhs = constraint["valor"]
            lhs = np.dot(coefficients, x0)
            
            if sign == "<=" and lhs > rhs:
                return False
            elif sign == ">=" and lhs < rhs:
                return False
            elif sign == "==" and not np.isclose(lhs, rhs, atol=1e-6):
                return False
        return True

    @classmethod
    def select_algorithm(cls, problem: ProblemInstance) -> str:
        """
        Selects the most appropriate algorithm based on the problem instance.
        
        If any variable is restricted to be integer, then Branch & Bound is used.
        For pure LP problems, the feasibility of the zero vector is used as a heuristic:
            - If feasible, use the Simplex method.
            - Otherwise, use the Dual Simplex method.
        
        Parameters:
            problem (ProblemInstance): The optimization problem instance.
            
        Returns:
            str: One of 'branch_and_bound', 'simplex', or 'dual_simplex'.
        """
        # Check for integer variables
        if any(problem.variables_integer):
            return "branch_and_bound"
        
        # For LP problems, check the feasibility of the zero vector
        if cls.is_zero_vector_feasible(problem):
            return "simplex"
        else:
            return "dual_simplex"