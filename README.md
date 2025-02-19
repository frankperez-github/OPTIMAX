# Optimax Project

## Running the Project

To run the project, follow these steps:

### 1. Build the Docker Image

First, build the Docker image for the project. Run the following command:

```bash
docker build -t optimax .
```

### 2. Run the `startup.sh` Script

After building the image, execute the `startup.sh` script to initialize the project and start the necessary services. Run:

```bash
./startup.sh
```

---

## Important Notes on the Solver and Method Change:

- The `highs` method in the `linprog` solver (from `scipy.optimize`) **does not accept a callback**.
  - If you want to track the convergence and visualize the progress(avoiding the auto selection of method), make the following changes:
    1. In `solver.py`, change the `method` argument from `method=method` to `method="simplex"`.
    2. Uncomment the line `callback=callback` on **line 70** in `solver.py`.

This will enable tracking and plotting the convergence graph.

---

## What is Optimax and How It Works

**Optimax** is a tool for solving optimization problems. It supports both **Linear Programming (LP)** and **Integer Linear Programming (ILP)** problems.

### Methods:

1. **Simplex**: A widely-used method for solving LP problems by iterating over feasible solutions to find the optimal one.
2. **Dual Simplex**: A variation of the simplex method that starts from an optimal solution and iterates toward a feasible one.
3. **Branch and Bound**: Used for solving ILP problems, this method involves breaking the problem into smaller subproblems and systematically eliminating infeasible solutions.

Optimax can automatically select the best algorithm for a given problem and provides tools for visualizing the solution, including the feasible region and convergence of the optimization process.

---

That's it! This should help you run the project smoothly and understand the core functionality. Let me know if you need any more details!
