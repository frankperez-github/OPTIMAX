def validate_dimensions(problem_instance):
    """
    Validates that the dimensions of the objective function and constraints match.

    Raises:
        ValueError: If a constraint's coefficient length does not match the number of variables.
    """
    num_vars = len(problem_instance.function_objective)
    for constraint in problem_instance.constraints:
        if len(constraint.get("coeficientes", [])) != num_vars:
            raise ValueError("Mismatch in dimensions: each constraint's coefficients length must match number of variables.")
    return True

def format_solution(solution):
    """
    Formats the solution dictionary into a human-readable string.

    Parameters:
        solution (dict): The solution dictionary.
        
    Returns:
        str: A formatted string representation of the solution.
    """
    if "variables" in solution:
        vars_str = ", ".join([f"x{i} = {val:.2f}" for i, val in enumerate(solution["variables"])])
    else:
        vars_str = "No variable assignments available."
    optimal_value = solution.get("optimal_value", "N/A")
    status = solution.get("status", "Unknown")
    return f"Status: {status}\nOptimal Value: {optimal_value}\nVariables: {vars_str}"
