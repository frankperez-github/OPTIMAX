import unittest
from optimax.parser import ProblemInstance
from optimax.solver import Solver

class TestSolver(unittest.TestCase):
    def test_solver_lp(self):
        json_input = '''
        {
            "objetivo": "maximizar",
            "funcion_objetivo": [5, 3],
            "restricciones": [
                {"coeficientes": [2, 1], "signo": "<=", "valor": 10},
                {"coeficientes": [1, 2], "signo": "<=", "valor": 8}
            ],
            "variables_enteras": [false, false]
        }
        '''
        problem = ProblemInstance.from_json(json_input)
        result = Solver.solve(problem, "simplex")
        self.assertEqual(result.get("status", "").lower(), "optimal")
        # The expected optimal value is 26 (5*4 + 3*2)
        self.assertAlmostEqual(result["optimal_value"], 26, places=2)
        self.assertAlmostEqual(result["variables"][0], 4, places=2)
        self.assertAlmostEqual(result["variables"][1], 2, places=2)

    def test_solver_ilp(self):
        json_input = '''
        {
            "objetivo": "maximizar",
            "funcion_objetivo": [5, 3],
            "restricciones": [
                {"coeficientes": [2, 1], "signo": "<=", "valor": 10},
                {"coeficientes": [1, 2], "signo": "<=", "valor": 8}
            ],
            "variables_enteras": [true, false]
        }
        '''
        problem = ProblemInstance.from_json(json_input)
        result = Solver.solve(problem, "branch_and_bound")
        self.assertEqual(result.get("status", "").lower(), "optimal")
        # Ensure that the integer variable is indeed an integer (or very close to it)
        self.assertEqual(round(result["variables"][0]), result["variables"][0])
        self.assertAlmostEqual(result["optimal_value"], 26, places=2)

if __name__ == '__main__':
    unittest.main()
