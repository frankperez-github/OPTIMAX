import json
from typing import Dict, List

class ProblemInstance:
    def __init__(self, objective: str, function_objective: List[float], constraints: List[Dict], variables_integer: List[bool]):
        self.objective = objective.lower()
        self.function_objective = function_objective
        self.constraints = constraints
        self.variables_integer = variables_integer
        self.validate()

    def validate(self):
        assert self.objective in ["maximizar", "minimizar"], "Objective must be 'maximizar' or 'minimizar'"
        assert len(self.function_objective) == len(self.variables_integer), "Mismatch between objective function and variable count"
        for constraint in self.constraints:
            assert len(constraint["coeficientes"]) == len(self.function_objective), "Constraint coefficient count mismatch"

    @classmethod
    def from_json(cls, json_input: str):
        data = json.loads(json_input)
        return cls(
            objective=data["objetivo"],
            function_objective=data["funcion_objetivo"],
            constraints=data["restricciones"],
            variables_integer=data.get("variables_enteras", [])
        )