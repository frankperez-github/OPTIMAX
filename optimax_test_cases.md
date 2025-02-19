# OPTIMAX Test Cases

## **Problem 1: Simple LP Maximization**

### **Problem:**

Maximize:

\[ Z = 4x_0 + 3x_1  \]

Subject to:

\[ x_0 + 2x_0 \leq 8 \]
\[ 3x_0 + x_0 \leq 9 \]
\[ x_0, x_0 \geq 0 \]

### **JSON Representation:**

```json
{
    "objetivo": "maximizar",
    "funcion_objetivo": [4, 3],
    "restricciones": [
        {"coeficientes": [1, 2], "signo": "<=", "valor": 8},
        {"coeficientes": [3, 1], "signo": "<=", "valor": 9}
    ],
    "variables_enteras": [false, false]
}
```

### **Expected Solution:**

\[ x_0 = 2, \quad x_0 = 3, \quad Z = 17 \]

---

## **Problem 2: Simple LP Minimization**

### **Problem:**

Minimize:

\[ Z = 6x_0 + 8x_1  \]

Subject to:

\[ 5x_0 + 2x_1  \geq 10 \]
\[ x_0 + 3x_1  \geq 6 \]
\[ x_0, x_1  \geq 0 \]

### **JSON Representation:**

```json
{
    "objetivo": "minimizar",
    "funcion_objetivo": [6, 8],
    "restricciones": [
        {"coeficientes": [5, 2], "signo": ">=", "valor": 10},
        {"coeficientes": [1, 3], "signo": ">=", "valor": 6}
    ],
    "variables_enteras": [false, false]
}
```

### **Expected Solution:**

\[ x_0 = 1.38, \quad x_1  = 1.538, \quad Z = 20.62 \]

---

## **Problem 3: ILP with Integer Variables**

### **Problem:**

Maximize:

\[ Z = 7x_0 + 5x_1  \]

Subject to:

\[ 2x_0 + 3x_1  \leq 12 \]
\[ 4x_0 + x_1  \leq 10 \]
\[ x_0, x_1  \text{ are integers} \geq 0 \]

### **JSON Representation:**

```json
{
    "objetivo": "maximizar",
    "funcion_objetivo": [7, 5],
    "restricciones": [
        {"coeficientes": [2, 3], "signo": "<=", "valor": 12},
        {"coeficientes": [4, 1], "signo": "<=", "valor": 10}
    ],
    "variables_enteras": [true, true]
}
```

### **Expected Solution:**

\[ x_0 = 2, \quad x_1  = 2, \quad Z = 24 \]

---

## **Problem 4: ILP with Mixed Integer Variables**

### **Problem:**

Maximize:

\[ Z = 9x_0 + 4x_1  \]

Subject to:

\[ 3x_0 + x_1  \leq 15 \]
\[ x_0 + 2x_1  \leq 8 \]
\[ x_0 \text{ is integer, } x_1  \text{ is continuous} \]

### **JSON Representation:**

```json
{
    "objetivo": "maximizar",
    "funcion_objetivo": [9, 4],
    "restricciones": [
        {"coeficientes": [3, 1], "signo": "<=", "valor": 15},
        {"coeficientes": [1, 2], "signo": "<=", "valor": 8}
    ],
    "variables_enteras": [true, false]
}
```

### **Expected Solution:**

\[ x_0 = 5, \quad x_1  = 0, \quad Z = 45 \]

---

## **Problem 5: Infeasible Problem**

### **Problem:**

Maximize:

\[ Z = 5x_0 + 2x_1  \]

Subject to:

\[ x_0 + x_1  \leq 3 \]
\[ x_0 + x_1  \geq 5 \]

### **JSON Representation:**

```json
{
    "objetivo": "maximizar",
    "funcion_objetivo": [5, 2],
    "restricciones": [
        {"coeficientes": [1, 1], "signo": "<=", "valor": 3},
        {"coeficientes": [1, 1], "signo": ">=", "valor": 5}
    ],
    "variables_enteras": [false, false]
}
```

### **Expected Solution:**

```
status: "Infeasible"
```
