import unittest
from optimax.parser import ProblemInstance

class TestParser(unittest.TestCase):
    def test_valid_json(self):
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
        self.assertEqual(problem.objective, "maximizar")
        self.assertEqual(problem.function_objective, [5, 3])
        self.assertEqual(len(problem.constraints), 2)
        self.assertEqual(problem.variables_integer, [False, False])
    
    def test_invalid_objective(self):
        json_input = '''
        {
            "objetivo": "maximize",
            "funcion_objetivo": [5, 3],
            "restricciones": [
                {"coeficientes": [2, 1], "signo": "<=", "valor": 10}
            ],
            "variables_enteras": [false, false]
        }
        '''
        with self.assertRaises(AssertionError):
            _ = ProblemInstance.from_json(json_input)
    
    def test_constraint_dimension_mismatch(self):
        json_input = '''
        {
            "objetivo": "maximizar",
            "funcion_objetivo": [5, 3, 2],
            "restricciones": [
                {"coeficientes": [2, 1], "signo": "<=", "valor": 10}
            ],
            "variables_enteras": [false, false, false]
        }
        '''
        with self.assertRaises(AssertionError):
            _ = ProblemInstance.from_json(json_input)

if __name__ == '__main__':
    unittest.main()
